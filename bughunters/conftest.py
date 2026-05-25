import json
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from bughunters.data.constants import MANAGER_USER, TIMEOUTS, URLS
from bughunters.pages import Pages

API_LOGIN_URL = "https://stg.polakohedonist.club/api/auth/login"
_AUTH_COOKIE_DOMAIN = "stg.polakohedonist.club"


# ── Browser (session-scoped) ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        yield browser


# ── Unauthenticated fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


# ── API-based auth (primary) ──────────────────────────────────────────────────

def _api_login(browser: Browser) -> Page:
    """
    Authenticates via POST /api/auth/login, injects the access_token cookie
    on the correct domain, and navigates directly to the personal-information page.

    The client app (stg-client.polakohedonist.club) does a 301 → stg.polakohedonist.club,
    so the cookie must be set on stg.polakohedonist.club.
    No UI interaction needed — language-independent.
    """
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    page = ctx.new_page()

    # 1. Call the API to get a fresh access token
    resp = page.request.post(
        API_LOGIN_URL,
        data=json.dumps({
            "email": MANAGER_USER["email"],
            "password": MANAGER_USER["password"],
        }),
        headers={"Content-Type": "application/json"},
    )
    assert resp.ok, f"API login failed: {resp.status} {resp.text()}"
    body = resp.json()
    access_token = body["data"]["access_token"]

    # 2. Inject access_token cookie on the API/app domain
    ctx.add_cookies([
        {
            "name": "access_token",
            "value": access_token,
            "domain": _AUTH_COOKIE_DOMAIN,
            "path": "/",
            "httpOnly": False,
            "secure": True,
            "sameSite": "Lax",
        }
    ])

    # 3. Navigate directly to personal-information — the app reads the cookie server-side
    page.goto(URLS["personal_info"], timeout=TIMEOUTS["navigation"])
    # Confirm we landed on the right page (not redirected to login)
    page.locator("input[name='first_name']").wait_for(state="visible", timeout=TIMEOUTS["element"])

    return page, ctx


@pytest.fixture(scope="function")
def authenticated_page(browser_instance: Browser) -> Page:
    """
    Primary fixture: API login → cookie injection → navigate to personal-info.
    One login per test, no UI modal interaction.
    """
    page, ctx = _api_login(browser_instance)
    yield page
    ctx.close()


# ── UI-based auth (fallback) ──────────────────────────────────────────────────

def _ui_login(page: Page) -> None:
    """
    Fallback: performs login via the header modal.
    Use when API auth is unavailable or needs to be tested explicitly.
    Language-independent: structural selectors only.
    """
    page.goto(URLS["home"], timeout=TIMEOUTS["navigation"])
    page.wait_for_timeout(1500)
    page.locator("button.ml-4").click()
    page.wait_for_timeout(1000)
    page.locator("input[name='email']").fill(MANAGER_USER["email"])
    page.locator("input[name='password']").fill(MANAGER_USER["password"])
    page.locator("button[type='submit'].btn-accent").click()
    page.locator("a[href*='/user']").first.wait_for(state="visible", timeout=TIMEOUTS["navigation"])


@pytest.fixture(scope="function")
def authenticated_page_ui(browser_instance: Browser) -> Page:
    """
    Fallback fixture: UI login via header modal.
    Slower than authenticated_page but tests the full login flow.
    """
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    p = ctx.new_page()
    _ui_login(p)
    yield p
    ctx.close()


# ── Page-object facades ───────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def pages(page: Page) -> Pages:
    return Pages(page)


@pytest.fixture(scope="function")
def auth_pages(authenticated_page: Page) -> Pages:
    return Pages(authenticated_page)


@pytest.fixture(scope="function")
def auth_pages_ui(authenticated_page_ui: Page) -> Pages:
    """Page-object facade backed by UI-authenticated page (fallback)."""
    return Pages(authenticated_page_ui)

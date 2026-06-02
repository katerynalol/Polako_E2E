import json
import os
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from bughunters.data.constants import MANAGER_USER, TIMEOUTS, URLS
from bughunters.pages import Pages
from bughunters.pages.auth_page import AuthPage
from bughunters.pages.personal_info_page import PersonalInfoPage

API_LOGIN_URL = "https://stg.polakohedonist.club/api/auth/login"
_AUTH_COOKIE_DOMAIN = "stg.polakohedonist.club"


# ── Browser (session-scoped) ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as pw:
        # headless=True in CI (env var CI is set by GitHub Actions), False locally
        headless = os.environ.get("CI", "false").lower() == "true"
        browser = pw.chromium.launch(headless=headless)
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
    """Fallback: performs login via the header modal using POM."""
    auth_page = AuthPage(page)
    auth_page.login(MANAGER_USER["email"], MANAGER_USER["password"])
    auth_page.profile_link.wait_for(state="visible", timeout=TIMEOUTS["navigation"])


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
def auth_page(page: Page) -> AuthPage:
    """Возвращает чистый объект страницы авторизации для неавторизованной зоны"""
    return AuthPage(page)


@pytest.fixture(scope="function")
def auth_page_authenticated(authenticated_page: Page) -> AuthPage:
    """Возвращает страницу авторизации, привязанную к АВТОРИЗОВАННОМУ контексту (к той же вкладке)"""
    return AuthPage(authenticated_page)


@pytest.fixture(scope="function")
def auth_page_ui(authenticated_page_ui: Page) -> AuthPage:
    """Возвращает страницу авторизации для UI-авторизованного контекста"""
    return AuthPage(authenticated_page_ui)


@pytest.fixture(scope="function")
def personal_info_page(authenticated_page: Page) -> PersonalInfoPage:
    """Возвращает страницу личной информации, которая уже открыта после API-авторизации"""
    return PersonalInfoPage(authenticated_page)
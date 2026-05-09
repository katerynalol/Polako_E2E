import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from bughunters.data.constants import MANAGER_USER, TIMEOUTS, URLS
from bughunters.pages import Pages


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(
        viewport={"width": 1280, "height": 800},
        base_url=URLS["home"],
    )
    ctx.set_default_timeout(TIMEOUTS["default"])
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Page:
    """Страница с активной сессией менеджера."""
    Pages(page).auth.login(MANAGER_USER["email"], MANAGER_USER["password"])
    page.wait_for_selector(
        "button:has-text('Профиль'), a:has-text('Профиль')",
        timeout=TIMEOUTS["navigation"],
    )
    return page


@pytest.fixture(scope="function")
def pages(page: Page) -> Pages:
    return Pages(page)


@pytest.fixture(scope="function")
def auth_pages(authenticated_page: Page) -> Pages:
    return Pages(authenticated_page)
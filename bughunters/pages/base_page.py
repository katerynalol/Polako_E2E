from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from bughunters.data.constants import TIMEOUTS


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._timeout = TIMEOUTS["element"]

    def navigate(self, url: str) -> None:
        self.page.goto(url, timeout=TIMEOUTS["navigation"])

    def current_url(self) -> str:
        return self.page.url

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        loc = self.page.locator(selector)
        loc.clear()
        loc.fill(value)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_visible(self, selector: str, timeout: int | None = None) -> Locator:
        loc = self.page.locator(selector)
        loc.wait_for(state="visible", timeout=timeout or self._timeout)
        return loc

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

    # ── Header helpers (available on any page) ────────────────────────────
    def click_login_button(self) -> None:
        self.page.locator("button:has-text('Войти'), button:has-text('Login')").first.click()

    def click_profile_button(self) -> None:
        self.page.locator("button:has-text('Профиль'), a:has-text('Профиль')").first.click()

    def is_logged_in(self, timeout: int = 10_000) -> bool:
        try:
            self.page.locator(
                "button:has-text('Профиль'), a:has-text('Профиль')"
            ).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def logout(self) -> None:
        self.click_profile_button()
        self.page.locator("button:has-text('Выйти'), a:has-text('Выйти')").click()
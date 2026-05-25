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

    # ── Header helpers ────────────────────────────────────────────────────

    def click_login_button(self) -> None:
        # Unique class on the header login button — language-independent
        self.page.locator("button.ml-4").first.click()

    def click_profile_button(self) -> None:
        # After login the header shows a link to /user with avatar initial + "Profile"
        self.page.locator("a[href*='/user']").first.click()

    def is_logged_in(self, timeout: int = 10_000) -> bool:
        try:
            # Profile link appears in header only when authenticated
            self.page.locator("a[href*='/user']").first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def logout(self) -> None:
        # Sidebar logout button — data-slot="button" + unique position
        self.page.locator("a[href*='/user']").first.click()
        self.page.wait_for_timeout(1000)
        # Logout button is the only button with group/button class that is NOT type=submit
        self.page.locator("button[type='button'][class*='group/button']").last.click()
from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS, TIMEOUTS


class PersonalInfoPage(BasePage):
    # ── Form fields — real name attributes from DOM ───────────────────────
    _FIRST_NAME       = "input[name='first_name']"
    _LAST_NAME        = "input[name='last_name']"
    _EMAIL            = "input[name='email']"
    _PHONE            = "input[name='phone']"
    _INSTAGRAM        = "input[name='instagram']"
    _TELEGRAM         = "input[name='telegram']"

    # ── Actions ───────────────────────────────────────────────────────────
    # Two submit buttons on the page: first = save profile, second = change password
    _SAVE_BTN         = "button[type='submit'][data-slot='button']:first-of-type"
    _NEW_PASSWORD     = "input[name='new_password']"
    _CONFIRM_PASSWORD = "input[name='confirm_password']"
    _CHANGE_PWD_BTN   = "button[type='submit'][data-slot='button']:last-of-type"

    # ── Feedback ──────────────────────────────────────────────────────────
    # Toast text observed: "Profile saved" — but we match by role to stay language-agnostic
    _SUCCESS_TOAST    = "[role='status'], [class*='toast'], [class*='Toast'], [class*='success']"

    # ── Sidebar navigation ────────────────────────────────────────────────
    _NAV_PURCHASES    = "a[href$='/user/purchases']"
    _NAV_BALANCE      = "a[href*='/user/balance']"
    _NAV_EVENTS       = "a[href*='/user/events']"
    # Logout: unique combination — data-slot=button, type=button, accent background.
    # Only one such button exists on the personal-info page (confirmed in DOM inspection).
    _LOGOUT_BTN       = "button[type='button'][class*='bg-accent']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["personal_info"])

    def get_first_name(self) -> str:
        return self.page.locator(self._FIRST_NAME).input_value()

    def get_email(self) -> str:
        return self.page.locator(self._EMAIL).input_value()

    def update_profile(self, first_name: str = None, last_name: str = None,
                       phone: str = None, instagram: str = None, telegram: str = None) -> None:
        if first_name is not None:
            self.fill(self._FIRST_NAME, first_name)
        if last_name is not None:
            self.fill(self._LAST_NAME, last_name)
        if phone is not None:
            self.fill(self._PHONE, phone)
        if instagram is not None:
            self.fill(self._INSTAGRAM, instagram)
        if telegram is not None:
            self.fill(self._TELEGRAM, telegram)
        self.page.locator("button[type='submit']").first.click()

    def is_saved(self, timeout: int = 5_000) -> bool:
        """Returns True if a success toast/notification appears after save."""
        try:
            self.page.locator(self._SUCCESS_TOAST).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def change_password(self, new_password: str) -> None:
        self.fill(self._NEW_PASSWORD, new_password)
        self.fill(self._CONFIRM_PASSWORD, new_password)
        self.page.locator("button[type='submit']").last.click()

    def navigate_to_purchases(self) -> None:
        self.click(self._NAV_PURCHASES)

    def navigate_to_balance(self) -> None:
        self.click(self._NAV_BALANCE)
from __future__ import annotations
from playwright.sync_api import expect
import re
from .base_page import BasePage
from bughunters.data.constants import URLS


class PersonalInfoPage(BasePage):
    _FIRST_NAME = "input[name='first_name']"
    _LAST_NAME = "input[name='last_name']"
    _EMAIL = "input[name='email']"
    _PHONE = "input[name='phone']"
    _INSTAGRAM = "input[name='instagram']"
    _TELEGRAM = "input[name='telegram']"
    _NEW_PASSWORD = "input[name='new_password']"
    _CONFIRM_PASSWORD = "input[name='confirm_password']"

    _SAVE_BTN = "button[type='submit'][data-slot='button']"
    _CHANGE_PWD_BTN = "button[type='submit'][data-slot='button']"
    _LOGOUT_BTN = "button.text-red-500, button:has-text('Выйти')"  # Сделали более гибким

    _NAV_PERSONAL_INFO = "a[href*='/user/personal-information']"
    _NAV_PURCHASES = "a[href*='/user/purchases']"

    _SUCCESS_TOAST = "[role='status'], [class*='toast'], [class*='Toast'], [class*='success']"

    def open(self) -> None:
        self.navigate(URLS["home"] + "/user/personal-information")

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
        self.page.locator(self._SAVE_BTN).first.click()

    def navigate_to_purchases(self) -> None:
        self.page.locator(self._NAV_PURCHASES).first.click()

    def navigate_to_personal_info(self) -> None:
        self.page.locator(self._NAV_PERSONAL_INFO).first.click()

    def click_logout(self) -> None:
        self.page.locator(self._LOGOUT_BTN).click()

    def verify_profile_fields_visible(self) -> None:
        for name in ("first_name", "last_name", "email", "phone", "instagram", "telegram"):
            expect(self.page.locator(f"input[name='{name}']")).to_be_visible()

    def verify_password_fields_visible(self) -> None:
        expect(self.page.locator(self._NEW_PASSWORD)).to_be_visible()
        expect(self.page.locator(self._CONFIRM_PASSWORD)).to_be_visible()

    def verify_sidebar_links_visible(self) -> None:
        expect(self.page.locator(self._NAV_PERSONAL_INFO).first).to_be_visible()
        expect(self.page.locator(self._NAV_PURCHASES).first).to_be_visible()

    def verify_logout_btn_visible(self) -> None:
        expect(self.page.locator(self._LOGOUT_BTN)).to_be_visible()

    def verify_success_toast_contains_text(self, pattern: str | re.Pattern) -> None:
        expect(self.page.locator("body")).to_have_text(pattern, ignore_case=True)

    def change_password(self, new_password: str) -> None:
        self.fill(self._NEW_PASSWORD, new_password)
        self.fill(self._CONFIRM_PASSWORD, new_password)
        self.page.locator(self._CHANGE_PWD_BTN).last.click()
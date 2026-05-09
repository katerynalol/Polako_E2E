from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS


class PersonalInfoPage(BasePage):
    _FIRST_NAME       = "input[name='firstName'], input[placeholder*='Имя']"
    _LAST_NAME        = "input[name='lastName'], input[placeholder*='Фамилия']"
    _EMAIL            = "input[name='email'], input[type='email']"
    _PHONE            = "input[name='phone'], input[type='tel']"
    _INSTAGRAM        = "input[name='instagram'], input[placeholder*='Instagram']"
    _TELEGRAM         = "input[name='telegram'], input[placeholder*='Telegram']"
    _SAVE_BTN         = "button:has-text('Сохранить')"
    _SUCCESS_TOAST    = "[class*='success'], :text('сохранён'), :text('saved')"
    _SAVE_DISABLED    = "button:has-text('Сохранить')[disabled]"
    _NEW_PASSWORD     = "input[name='newPassword'], input[placeholder*='новый пароль']"
    _CONFIRM_PASSWORD = "input[name='confirmPassword'], input[placeholder*='Подтвердите']"
    _CHANGE_PWD_BTN   = "button:has-text('Изменить пароль')"
    _LOGOUT_BTN       = "button:has-text('Выйти'), a:has-text('Выйти')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["personal_info"])

    def update_name(self, first_name: str, last_name: str) -> None:
        self.fill(self._FIRST_NAME, first_name)
        self.fill(self._LAST_NAME, last_name)
        self.click(self._SAVE_BTN)

    def update_email(self, email: str) -> None:
        self.fill(self._EMAIL, email)
        self.click(self._SAVE_BTN)

    def is_saved(self) -> bool:
        return self.page.locator(self._SUCCESS_TOAST).is_visible(timeout=5_000)

    def is_save_button_disabled(self) -> bool:
        return self.page.locator(self._SAVE_DISABLED).is_visible()

    def change_password(self, new_password: str) -> None:
        self.fill(self._NEW_PASSWORD, new_password)
        self.fill(self._CONFIRM_PASSWORD, new_password)
        self.click(self._CHANGE_PWD_BTN)

    def logout(self) -> None:
        self.click(self._LOGOUT_BTN)
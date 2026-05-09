from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS, TIMEOUTS


class AuthPage(BasePage):
    _EMAIL        = "input[name='email'], input[type='email']"
    _PASSWORD     = "input[name='password'], input[type='password']"
    _SUBMIT       = "button[type='submit']:has-text('Войти')"
    _ERROR        = "[class*='error'], .toast-error"
    _PROFILE_BTN  = "button:has-text('Профиль'), a:has-text('Профиль')"
    _REGISTER_LINK  = "span:has-text('нет аккаунта'), a:has-text('Регистрация')"
    _REG_FOR_USER    = "button:has-text('Для пользователя')"
    _REG_FOR_MANAGER = "button:has-text('Для организатора')"
    _FIRST_NAME   = "input[name='firstName'], input[placeholder*='Имя']"
    _LAST_NAME    = "input[name='lastName'], input[placeholder*='Фамилия']"
    _REG_SUBMIT   = "button[type='submit']:has-text('Зарегистрироваться')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["home"])

    def open_login_modal(self) -> None:
        self.click_login_button()
        self.wait_visible(self._EMAIL)

    def login(self, email: str, password: str) -> None:
        self.open()
        self.open_login_modal()
        self.fill(self._EMAIL, email)
        self.fill(self._PASSWORD, password)
        self.click(self._SUBMIT)
        # self.page.wait_for_timeout(1_500)

    def get_error_message(self) -> str:
        loc = self.page.locator(self._ERROR)
        return loc.inner_text() if loc.is_visible() else ""

    def open_register_user(self) -> None:
        self.open()
        self.open_login_modal()
        self.click(self._REGISTER_LINK)
        self.click(self._REG_FOR_USER)

    def open_register_manager(self) -> None:
        self.open()
        self.open_login_modal()
        self.click(self._REGISTER_LINK)
        self.click(self._REG_FOR_MANAGER)

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> None:
        self.open_register_user()
        self.fill(self._FIRST_NAME, first_name)
        self.fill(self._LAST_NAME, last_name)
        self.fill(self._EMAIL, email)
        self.fill(self._PASSWORD, password)
        self.click(self._REG_SUBMIT)
from playwright.sync_api import expect

from bughunters.data.constants import MANAGER_USER
from bughunters.pages.auth_page import AuthPage
from bughunters.pages.personal_info_page import PersonalInfoPage


class TestLoginHappyPath:
    def test_successful_login_shows_profile_link(self, auth_page: AuthPage) -> None:
        auth_page.login(MANAGER_USER["email"], MANAGER_USER["password"])
        expect(auth_page.profile_link).to_be_visible(timeout=10_000)


class TestLoginNegative:
    def test_wrong_password_shows_error(self, auth_page: AuthPage) -> None:
        auth_page.open()
        auth_page.open_login_modal()
        auth_page.fill_login_form(MANAGER_USER["email"], "wrong_password_123")
        auth_page.submit_login()
        expect(auth_page.profile_link).not_to_be_visible(timeout=3_000)


class TestLogout:
    def test_logout_removes_profile_link(
            self,
            personal_info_page: PersonalInfoPage,
            auth_page_authenticated: AuthPage
    ) -> None:
        personal_info_page.logout()
        expect(auth_page_authenticated.profile_link).not_to_be_visible(timeout=3_000)
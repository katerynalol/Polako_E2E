"""
Authentication tests — login via UI (modal flow).
API-based auth is covered in conftest.py (authenticated_page fixture).
"""
import pytest
from playwright.sync_api import Page
from bughunters.pages import Pages
from bughunters.data.constants import MANAGER_USER, URLS


class TestLoginHappyPath:
    def test_successful_login_shows_profile_link(self, pages: Pages) -> None:
        """Happy path: valid credentials → profile link appears in header."""
        pages.auth.login(MANAGER_USER["email"], MANAGER_USER["password"])
        # After login the header renders a link to /user — language-independent signal
        pages.auth.page.locator("a[href*='/user']").wait_for(state="visible", timeout=10_000)
        assert pages.auth.is_logged_in(), "Profile link not visible after successful login"


class TestLoginNegative:
    def test_wrong_password_shows_error(self, pages: Pages) -> None:
        """Invalid password → error feedback is shown."""
        pages.auth.open()
        pages.auth.open_login_modal()
        pages.auth.fill(pages.auth._EMAIL, MANAGER_USER["email"])
        pages.auth.fill(pages.auth._PASSWORD, "wrong_password_123")
        pages.auth.click(pages.auth._SUBMIT)
        pages.auth.page.wait_for_timeout(2000)
        # Either an error element appears OR the profile link does NOT appear
        assert not pages.auth.is_logged_in(timeout=3_000), \
            "Should NOT be logged in with wrong password"

    def test_empty_credentials_does_not_login(self, pages: Pages) -> None:
        """Submitting empty form should not authenticate the user."""
        pages.auth.open()
        pages.auth.open_login_modal()
        # Use JS click to bypass HTML5 required-field validation
        pages.auth.page.locator(pages.auth._SUBMIT).click(force=True)
        pages.auth.page.wait_for_timeout(2000)
        assert not pages.auth.is_logged_in(timeout=3_000), \
            "Should NOT be logged in with empty credentials"


class TestLogout:
    def test_logout_removes_profile_link(self, auth_pages_ui: Pages) -> None:
        """After logout the profile link must disappear from the header."""
        page = auth_pages_ui.auth.page
        assert auth_pages_ui.auth.is_logged_in(), "Must be logged in before testing logout"

        # Navigate to personal info page where the sidebar with logout is visible
        auth_pages_ui.personal_info.open()
        page.wait_for_timeout(1500)

        logout_btn = page.locator(auth_pages_ui.personal_info._LOGOUT_BTN)
        logout_btn.wait_for(state="visible", timeout=5_000)
        logout_btn.click()
        page.wait_for_timeout(2000)

        assert not auth_pages_ui.auth.is_logged_in(timeout=3_000), \
            "Profile link should not be visible after logout"
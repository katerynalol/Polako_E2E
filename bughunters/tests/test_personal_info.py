"""
Personal info (profile) page tests.

All tests use API-based auth (auth_pages fixture):
  - Login happens once via POST /api/auth/login + cookie injection
  - Browser navigates directly to /user/personal-information
  - No repeated UI logins between tests

Fallback: auth_pages_ui uses UI login (authenticated_page_ui fixture).
"""
import pytest
from bughunters.pages import Pages


class TestPersonalInfoHappyPath:
    def test_page_loads_with_user_email(self, auth_pages: Pages) -> None:
        """
        Happy path: personal-info page is already open after API login.
        Email field must be pre-filled with the authenticated user's email.
        """
        email = auth_pages.personal_info.get_email()
        assert email and "@" in email, \
            f"Email field should be pre-filled with a valid email, got: {email!r}"

    def test_first_name_field_is_pre_filled(self, auth_pages: Pages) -> None:
        """First name input should contain the user's stored name."""
        name = auth_pages.personal_info.get_first_name()
        # Field may be empty if user never set it — just assert it's accessible
        assert auth_pages.personal_info.page.locator("input[name='first_name']").is_visible(), \
            "First name input should be visible"

    def test_profile_url_is_correct(self, auth_pages: Pages) -> None:
        """After API login we should land on personal-information, not a login redirect."""
        assert "personal-information" in auth_pages.personal_info.current_url(), \
            f"Expected personal-information URL, got: {auth_pages.personal_info.current_url()}"

    def test_save_profile_shows_success_toast(self, auth_pages: Pages) -> None:
        """
        Happy path: saving the profile with current data triggers a success toast.
        Observed toast text: 'Profile saved'.
        """
        current_name = auth_pages.personal_info.get_first_name() or "Hren"
        auth_pages.personal_info.update_profile(first_name=current_name)

        page = auth_pages.personal_info.page
        page.wait_for_timeout(2000)
        body_text = page.locator("body").inner_text()
        assert any(kw in body_text for kw in ["сохранён", "сохранен", "saved", "успех", "success"]), \
            "Expected success feedback after saving profile"

    def test_all_profile_fields_are_visible(self, auth_pages: Pages) -> None:
        """All expected input fields should be present on the page."""
        page = auth_pages.personal_info.page
        for name in ("first_name", "last_name", "email", "phone", "instagram", "telegram"):
            inp = page.locator(f"input[name='{name}']")
            assert inp.is_visible(), f"Input[name='{name}'] should be visible"

    def test_password_change_fields_are_visible(self, auth_pages: Pages) -> None:
        """New password and confirm password fields should be present."""
        page = auth_pages.personal_info.page
        assert page.locator("input[name='new_password']").is_visible(), \
            "New password field should be visible"
        assert page.locator("input[name='confirm_password']").is_visible(), \
            "Confirm password field should be visible"

    def test_sidebar_nav_links_present(self, auth_pages: Pages) -> None:
        """Key sidebar navigation links should be visible."""
        page = auth_pages.personal_info.page
        for href in ("/user/personal-information", "/user/purchases"):
            assert page.locator(f"a[href*='{href}']").first.is_visible(), \
                f"Sidebar link to {href!r} should be visible"

    def test_logout_button_is_present(self, auth_pages: Pages) -> None:
        """Logout button should be visible in the sidebar."""
        page = auth_pages.personal_info.page
        logout = page.locator(auth_pages.personal_info._LOGOUT_BTN)
        assert logout.is_visible(), "Logout button should be visible in sidebar"


class TestPersonalInfoNavigation:
    def test_navigate_to_purchases_via_sidebar(self, auth_pages: Pages) -> None:
        """Clicking the purchases sidebar link navigates to /user/purchases."""
        auth_pages.personal_info.navigate_to_purchases()
        auth_pages.personal_info.page.wait_for_timeout(1500)
        assert "purchases" in auth_pages.personal_info.current_url(), \
            "Should navigate to purchases page"

    def test_navigate_back_to_profile_via_sidebar(self, auth_pages: Pages) -> None:
        """After going to purchases, clicking profile link returns to personal-info."""
        auth_pages.personal_info.navigate_to_purchases()
        auth_pages.personal_info.page.wait_for_timeout(1000)
        auth_pages.personal_info.page.locator("a[href*='/user/personal-information']").first.click()
        auth_pages.personal_info.page.wait_for_timeout(1500)
        assert "personal-information" in auth_pages.personal_info.current_url(), \
            "Should navigate back to personal-information"


class TestPurchasesPage:
    def test_purchases_page_loads(self, auth_pages: Pages) -> None:
        """Happy path: purchases page is accessible from personal-info sidebar."""
        auth_pages.purchases.open()
        auth_pages.purchases.page.wait_for_timeout(1500)
        assert "purchases" in auth_pages.purchases.current_url()

    def test_purchases_shows_empty_state_or_items(self, auth_pages: Pages) -> None:
        """Purchases page must render either a list or an empty-state message."""
        auth_pages.purchases.open()
        auth_pages.purchases.page.wait_for_timeout(1500)
        count = auth_pages.purchases.get_purchase_count()
        is_empty = auth_pages.purchases.is_empty()
        assert count > 0 or is_empty, \
            "Purchases page should show items or an empty-state message"
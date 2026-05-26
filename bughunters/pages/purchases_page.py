from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS


class PurchasesPage(BasePage):
    _PAGE_HEADING  = "h1, h2"
    # Sidebar nav link — language-independent
    _NAV_LINK      = "a[href*='/user/purchases']"
    # Empty state text observed: "Покупок пока нет"
    _EMPTY_STATE   = "py-8 text-center"
    # Purchase cards — look for list items or article elements in main content
    _PURCHASE_ITEM = "main li, main article, [class*='purchase'], [class*='order']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["purchases"])

    def get_purchase_count(self) -> int:
        return self.page.locator(self._PURCHASE_ITEM).count()

    def is_empty(self) -> bool:
        return self.page.locator(self._EMPTY_STATE).is_visible(timeout=5_000)
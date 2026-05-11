from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS


class PurchasesPage(BasePage):
    _PAGE_HEADING     = "h1, h2"
    _PURCHASE_ITEM    = "[class*='purchase-item'], [class*='purchaseItem']"
    _SEARCH_INPUT     = "input[placeholder*='поиск'], input[type='search']"
    _EMPTY_STATE      = ":text('ничего не найдено'), :text('нет покупок'), [class*='empty']"
    _PDF_BTN          = "a:has-text('PDF'), button:has-text('PDF'), :text('Скачать билеты')"
    _FISCAL_RECEIPT   = ":text('Фискальный чек')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["purchases"])

    def search(self, query: str) -> None:
        self.fill(self._SEARCH_INPUT, query)

    def clear_search(self) -> None:
        self.page.locator(self._SEARCH_INPUT).clear()

    def get_purchase_count(self) -> int:
        return self.page.locator(self._PURCHASE_ITEM).count()

    def is_empty(self) -> bool:
        return self.page.locator(self._EMPTY_STATE).is_visible()
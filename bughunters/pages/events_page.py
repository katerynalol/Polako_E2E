from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS


class EventsPage(BasePage):
    _CREATE_BTN    = "button:has-text('Создать мероприятие'), a:has-text('Создать мероприятие')"
    _EVENT_CARD    = "[class*='event-card'], [class*='eventCard']"
    _PUBLISH_BTN   = "button:has-text('Опубликовать')"
    _DRAFT_BTN     = "button:has-text('В черновик')"
    _PREVIEW_BTN   = "button:has-text('Предпросмотр')"
    _EDIT_BTN      = "button:has-text('Редактировать')"
    _COPY_LINK_BTN = "button:has-text('Скопировать ссылку')"
    _BACK_BTN      = "a:has-text('Назад к мероприятиям'), button:has-text('Назад')"
    _EMPTY_STATE   = "[class*='empty'], :text('нет мероприятий')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["events_list"])

    def click_create(self) -> None:
        self.click(self._CREATE_BTN)

    def click_edit(self, index: int = 0) -> None:
        self.page.locator(self._EDIT_BTN).nth(index).click()

    def click_publish(self, index: int = 0) -> None:
        self.page.locator(self._PUBLISH_BTN).nth(index).click()

    def click_draft(self, index: int = 0) -> None:
        self.page.locator(self._DRAFT_BTN).nth(index).click()

    def click_preview(self, index: int = 0) -> None:
        self.page.locator(self._PREVIEW_BTN).nth(index).click()

    def click_copy_link(self, index: int = 0) -> None:
        self.page.locator(self._COPY_LINK_BTN).nth(index).click()

    def go_back_from_preview(self) -> None:
        self.click(self._BACK_BTN)

    def get_event_count(self) -> int:
        return self.page.locator(self._EVENT_CARD).count()

    def is_empty(self) -> bool:
        return self.page.locator(self._EMPTY_STATE).is_visible()
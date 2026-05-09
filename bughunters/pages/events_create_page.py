from __future__ import annotations
from playwright.sync_api import Page
from .events_page import EventsPage        # ← наследование
from bughunters.data.constants import URLS


class EventsCreatePage(EventsPage):
    """Inherits EventsPage — переиспользует click_create, EVENT_CARD и пр."""

    _TITLE        = "input[name='title'], input[placeholder*='Название']"
    _DESCRIPTION  = "textarea[name='description'], textarea[placeholder*='Описание']"
    _DATE         = "input[name='date'], input[type='date']"
    _TIME         = "input[name='time'], input[type='time']"
    _LOCATION     = "input[name='location'], input[placeholder*='Место']"
    _CAPACITY     = "input[name='capacity'], input[placeholder*='Вместимость']"
    _SAVE_BTN             = "button:has-text('Сохранить')"
    _SUCCESS_TOAST        = "[class*='success'], :text('создано'), :text('сохранено')"
    _PUBLISH_FROM_FORM    = "button:has-text('Опубликовать')"
    _PREVIEW_FROM_FORM    = "button:has-text('Предпросмотр')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["events_create"])

    def fill_form(self, title: str, description: str = "",
                  date: str = "", time: str = "",
                  location: str = "", capacity: str = "") -> None:
        self.fill(self._TITLE, title)
        if description: self.fill(self._DESCRIPTION, description)
        if date:        self.fill(self._DATE, date)
        if time:        self.fill(self._TIME, time)
        if location:    self.fill(self._LOCATION, location)
        if capacity:    self.fill(self._CAPACITY, capacity)

    def save(self) -> None:
        self.click(self._SAVE_BTN)

    def create_event(self, title: str, description: str = "",
                     date: str = "", location: str = "") -> None:
        self.fill_form(title=title, description=description,
                       date=date, location=location)
        self.save()

    def is_saved(self) -> bool:
        return self.page.locator(self._SUCCESS_TOAST).is_visible(timeout=5_000)

    def publish_from_form(self) -> None:
        self.click(self._PUBLISH_FROM_FORM)

    def preview_from_form(self) -> None:
        self.click(self._PREVIEW_FROM_FORM)
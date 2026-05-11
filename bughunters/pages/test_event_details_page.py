# Страница конкретного события
from playwright.sync_api import Page, expect
import re


class EventPage:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator("h1").first


        self.plus_button = page.locator("button").filter(
            has=page.locator("svg")          # кнопка с иконкой +
        ).and_(page.locator(":has-text('+')")).first



        self.buy_button = page.get_by_role("button").filter(
            has_text=re.compile("Buy|Купить", re.I)
        ).first

    def open(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def check_page_loaded(self):
        expect(self.title).to_be_visible(timeout=15000)

    def add_ticket(self, times: int = 1):
        expect(self.plus_button).to_be_visible(timeout=15000)
        for _ in range(times):
            self.plus_button.click()
            self.page.wait_for_timeout(500)

    def check_buy_button(self):
        expect(self.buy_button).to_be_visible(timeout=15000)


def test_event_page(page: Page):
    event = EventPage(page)

    event.open("https://polakohedonist.club/en/events/5ebacd6a-c977-411c-a030-b70f68e68faa")

    event.check_page_loaded()
    event.page.wait_for_timeout(2000)

    event.add_ticket(1)
    event.check_buy_button()


def test_event_page(page: Page):
    event = EventPage(page)
    event.open("https://polakohedonist.club/en/events/5ebacd6a-c977-411c-a030-b70f68e68faa")

    print("Все кнопки на странице:")
    buttons = page.locator("button").all()
    for i, btn in enumerate(buttons[:15]):  # первые 15
        text = btn.inner_text().strip()[:50]
        classes = btn.get_attribute("class")
        print(f"{i}: '{text}' | classes: {classes}")

    event.check_page_loaded()
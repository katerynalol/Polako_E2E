# редактирование ивентов

from playwright.sync_api import Page, expect
import re


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, email: str, password: str):
        self.page.goto("https://polakohedonist.club/ru", wait_until="networkidle")

        print("🔍 Нажимаем кнопку 'Войти'...")


        login_btn = self.page.get_by_role("button").filter(
            has_text=re.compile(r"Войти|Login", re.I)
        ).first

        login_btn.click()
        print("✅ Кнопка нажата, ждём форму...")

        self.page.wait_for_timeout(5000)


        print("\n📋 === ДИАГНОСТИКА ===")
        inputs = self.page.locator("input").all()
        print(f"Найдено input полей: {len(inputs)}")

        for i, field in enumerate(inputs):
            try:
                field_type = field.get_attribute("type") or "-"
                field_name = field.get_attribute("name") or "-"
                field_placeholder = field.get_attribute("placeholder") or "-"
                print(f"  {i}: type={field_type} | name={field_name} | placeholder={field_placeholder}")
            except:
                pass


        email_field = self.page.locator(
            'input[type="email"], input[placeholder*="email" i], input[name*="email" i]').first
        if email_field.is_visible(timeout=3000):
            email_field.fill(email)
            print("✅ Поле email заполнено")
        else:
            print("❌ Поле email не найдено")



def test_edit_event(page: Page):  # ← важно: test_ в начале
    login = LoginPage(page)
    login.login("hrensgori@polako.ru", "polako765")

    print("🏁 Тест завершён (пока только авторизация)")
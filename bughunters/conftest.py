import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def auth_page(browser):
    context = browser.new_context()
    page = context.new_page()

    # 1. Открываем главную страницу
    page.goto("https://stg.polakohedonist.club/ru")

    # 2. Кликаем на кнопку Войти
    page.click("button:has-text('Войти'), a:has-text('Войти')")

    # 3. Вводим email и пароль напрямую строками
    page.fill("input[name='email'], input[type='email']", "mierkulova.tech@gmail.com")
    page.fill("input[name='password'], input[type='password']", "polako567")

    # 4. Нажимаем кнопку Войти в форме
    page.click("button[type='submit']:has-text('Войти')")

    # 5. ИСПРАВЛЕНО: Ждём кнопку "Профиль" — она появляется на экране сразу же!
    page.wait_for_selector("button:has-text('Профиль'), a:has-text('Профиль')", state="visible", timeout=15_000)

    yield page
    context.close()
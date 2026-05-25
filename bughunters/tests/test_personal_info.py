from bughunters.pages.personal_info_page import PersonalInfoPage

def test_happy_path_personal_info(auth_page):
    """Тест проверяет успешный вход в ЛК и обновление имени (Happy Path)"""
    profile_page = PersonalInfoPage(auth_page)
    profile_page.open()
    assert profile_page.check_user_is_authorized() == True, "Пользователь не авторизован!"
    profile_page.update_name(first_name="Турбо", last_name="Тест")
    assert profile_page.is_saved() == True, "Уведомление об успешном сохранении не появилось!"

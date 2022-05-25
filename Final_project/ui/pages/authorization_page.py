import allure
from selenium.common.exceptions import TimeoutException
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from ui.locators import AuthorizationPageLocators


class ValidationError(Exception):
    pass


class AuthorizationPage(BasePage):
    locators = AuthorizationPageLocators()

    @allure.step('Авторизация: Username: {username}. Password: {password}')
    def login(self, username, password):
        self.click(self.locators.USERNAME)
        self.send_message(self.locators.USERNAME, username)
        self.click(self.locators.PASSWORD)
        self.send_message(self.locators.PASSWORD, password)
        self.click(self.locators.LOGIN_BUTTON)

        if self.driver.current_url == 'http://0.0.0.0:9999/welcome/':
            with allure.step('Авторизация успешна. Переход на главную страницу'):
                return MainPage(self.driver)
        else:
            with allure.step('Авторизация не удалась :('):
                pass

    @allure.step('Проверка валидации полей при авторизации')
    def check_fields_validation(self):
        try:
            self.find(self.locators.USERNAME, timeout=2)
            self.find(self.locators.PASSWORD, timeout=2)
        except TimeoutException:
            raise ValidationError('Валидация не пройдена')

    @allure.step('Переход с авторизации на регистрацию')
    def go_to_registration_page(self):
        self.click(self.locators.REGISTRATION_BUTTON)
        if self.driver.current_url == 'http://0.0.0.0:9999/reg':
            return RegistrationPage(self.driver)

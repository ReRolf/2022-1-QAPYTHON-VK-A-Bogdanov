import allure
from selenium.common.exceptions import TimeoutException
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage

from ui.locators import RegistrationPageLocators


class ValidationError(Exception):
    pass


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()

    @allure.step('Проверка валидации регистрации')
    def check_fields_validation(self):
        try:
            self.find(self.locators.REG_USERNAME, 2)
            self.find(self.locators.REG_EMAIL_VALID, 2)
            self.find(self.locators.REG_PASSWORD, 2)
            self.find(self.locators.REPEAT_PASSWORD_VALID, 2)
            self.find(self.locators.ACCEPT_CHECKBOX, 2)
        except TimeoutException:
            raise ValidationError('Валидация не пройдена')

    @allure.step('Регистрация. Username: {username}. Password: {password}')
    def register(self, username, email, password, repeat_password):
        self.click(self.locators.REG_USERNAME)
        self.send_message(self.locators.REG_USERNAME, username)
        self.click(self.locators.REG_EMAIL)
        self.send_message(self.locators.REG_EMAIL, email)
        self.click(self.locators.REG_PASSWORD)
        self.send_message(self.locators.REG_PASSWORD, password)
        self.click(self.locators.REPEAT_PASSWORD)
        self.send_message(self.locators.REPEAT_PASSWORD, repeat_password)
        self.click(self.locators.ACCEPT_CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)

        if self.driver.current_url == 'http://0.0.0.0:9999/welcome/':
            with allure.step('Регистрация прошла успешно. Переход на главную страницу.'):
                return MainPage(self.driver)
        else:
            with allure.step('Регистрация не удалась'):
                pass

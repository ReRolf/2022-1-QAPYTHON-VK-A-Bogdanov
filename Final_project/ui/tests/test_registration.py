import pytest
import allure
from selenium.common.exceptions import TimeoutException

from ui.fixtures import *
from ui.tests.base import BaseCase
from ui.pages.base_page import LocatorNotFoundError


@allure.feature('Тесты на UI')
@allure.story('Тесты на регистрацию')
class TestRegistrationPage(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def go_to_registration(self, driver):
        AuthorizationPage(driver).go_to_registration_page()

    @pytest.mark.UI
    def test_fields_validation(self, setup):
        self.registration_page.check_fields_validation()

    @pytest.mark.UI
    def test_correct_registration(self, setup, fake_data, mysql_client):
        self.registration_page.register(username=fake_data['username'], email=fake_data['email'],
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        self.main_page.find(self.main_page.locators.LOGGED_AS)

        user = mysql_client.select_by_username(fake_data['username'])
        assert user.username == fake_data['username']
        assert user.email == fake_data['email']
        assert user.password == fake_data['password']
        assert user.access == 1

    @pytest.mark.UI
    def test_invalid_username(self, setup, fake_data):
        self.registration_page.register(username=fake_data['username'][:3], email=fake_data['email'],
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        self.registration_page.find(self.registration_page.locators.USERNAME_ERROR, 2)

    @pytest.mark.UI
    def test_incorrect_email_length(self, setup, fake_data):
        self.registration_page.register(username=fake_data['username'], email=fake_data['email'][:3],
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        self.registration_page.find(self.registration_page.locators.INCORRECT_EMAIL_LENGTH, 2)

    @pytest.mark.UI
    def test_invalid_email(self, setup, fake_data):
        self.registration_page.register(username=fake_data['username'], email='artnovopolsky@mail',
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        self.registration_page.find(self.registration_page.locators.INVALID_EMAIL_ERROR, 2)

    @pytest.mark.UI
    def test_passwords_not_match(self, setup, fake_data):
        self.registration_page.register(username=fake_data['username'], email=fake_data['email'],
                                        password=fake_data['password'], repeat_password=fake_data['password'][::-1])
        self.registration_page.find(self.registration_page.locators.PASSWORD_NOT_MATCH_ERROR, 2)

    @pytest.mark.UI
    def test_all_fields_incorrect(self, setup):
        self.registration_page.register(username='user', email='incorrect',
                                        password='111', repeat_password='1')
        try:
            self.registration_page.find(self.registration_page.locators.ALL_FIELDS_INCORRECT_MESSAGE, 2)
        except TimeoutException:
            raise LocatorNotFoundError('Сообщение об ошибке некорректно')

    @pytest.mark.UI
    def test_register_existent_user(self, setup, fake_data, mysql_builder):
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        self.registration_page.register(username=fake_data['username'], email=fake_data['email'],
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        self.registration_page.find(self.registration_page.locators.USER_ALREADY_EXIST, 2)

    @pytest.mark.UI
    def test_register_with_existent_email(self, setup, fake_data, mysql_builder):
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        self.registration_page.register(username='Бибабоба', email=fake_data['email'],
                                        password='111', repeat_password='111')
        try:
            self.registration_page.find(self.registration_page.locators.EMAIL_ALREADY_IN_USE, 2)
        except TimeoutException:
            raise LocatorNotFoundError('Сообщение об ошибке некорректно!')

    @pytest.mark.UI
    def test_register_with_russian_username(self, setup, fake_data):
        self.registration_page.register(username='Бибабоба', email=fake_data['email'],
                                        password=fake_data['password'], repeat_password=fake_data['password'])
        try:
            self.registration_page.find(self.registration_page.locators.USERNAME_MUST_BE_IN_ENGLISH, 2)
        except TimeoutException:
            raise LocatorNotFoundError('Сообщение об ошибке некорректно')

    @pytest.mark.UI
    def test_go_to_authorization_page(self, setup):

        self.registration_page.click(self.registration_page.locators.GO_TO_LOGIN_BUTTON, 2)
        assert 'Welcome to the TEST SERVER' in self.authorization_page.driver.page_source

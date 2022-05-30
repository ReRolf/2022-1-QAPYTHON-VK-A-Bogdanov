import pytest
import allure
from ui.tests.base import BaseCase
from ui.fixtures import *


@allure.feature('Тесты на UI')
@allure.story('Тесты на авторизацию')
class TestAuthorizationPage(BaseCase):
    @pytest.mark.UI
    def test_fields_validation(self, setup):
        self.authorization_page.check_fields_validation()

    @pytest.mark.UI
    def test_fake_credentials(self, setup, fake_data):
        self.authorization_page.login(username=fake_data['username'], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.INVALID_ERROR_MESSAGE, 10)

    @pytest.mark.UI
    def test_invalid_username(self, setup, fake_data):
        self.authorization_page.login(username=fake_data['username'][:3], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.INCORRECT_ERROR_MESSAGE, 10)

    @pytest.mark.UI
    def test_valid_credentials(self, setup, fake_data, mysql_builder):
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        self.authorization_page.login(username=fake_data['username'],
                                      password=fake_data['password'])
        self.main_page.find(self.main_page.locators.LOGGED_AS, 10)

    @pytest.mark.UI
    def test_block_user_authorization(self, setup, fake_data, mysql_builder):
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'],
                               access=0)
        self.authorization_page.login(username=fake_data['username'], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.BLOCK_MESSAGE, 10)

    @pytest.mark.UI
    def test_go_to_registration_page(self, setup):
        self.authorization_page.go_to_registration_page()
        assert 'Registration' in self.registration_page.driver.page_source

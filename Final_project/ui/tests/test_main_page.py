import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from ui.fixtures import *
from ui.pages.base_page import LocatorNotFoundError
from ui.tests.base import BaseCase


@allure.feature('Тесты на UI')
@allure.story('Тесты главной страницы')
class TestMainPage(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def login(self, fake_data, setup, mysql_builder):

        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        AuthorizationPage(self.driver).login(username=fake_data['username'], password=fake_data['password'])
        self.username = fake_data['username']

    @pytest.mark.UI
    def test_TM_version_button(self):
        self.main_page.click(self.main_page.locators.TM_BUTTON, 2)
        self.main_page.find(self.main_page.locators.LOGGED_AS, 2)

    @pytest.mark.UI
    def test_home_button(self):
        self.main_page.click(self.main_page.locators.TM_BUTTON, 2)
        self.main_page.find(self.main_page.locators.LOGGED_AS, 2)

    @pytest.mark.UI
    def test_python_button(self):
        self.main_page.go_out_from_visible_locator(self.main_page.locators.PYTHON_BUTTON)
        assert 'Welcome to Python.org' in self.driver.title

    @pytest.mark.UI
    def test_python_history_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.PYTHON_BUTTON,
                                                  self.main_page.locators.PYTHON_HISTORY)
        assert 'History of Python - Wikipedia' in self.driver.title

    @pytest.mark.UI
    def test_about_flask_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.PYTHON_BUTTON,
                                                  self.main_page.locators.ABOUT_FLASK)
        assert 'Welcome to Flask' in self.driver.title

    @pytest.mark.UI
    def test_download_centos_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.LINUX_BUTTON,
                                                  self.main_page.locators.DOWNLOAD_CENTOS)
        assert 'CentOS' in self.driver.title

    @pytest.mark.UI
    def test_news_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.WIRESHARK_NEWS)
        assert 'Wireshark · News' in self.driver.title

    @pytest.mark.UI
    def test_download_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.DOWNLOAD_WIRESHARK)
        assert 'Wireshark · Go Deep.' in self.driver.title

    @pytest.mark.UI
    def test_examples_button(self):
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.TCPDUMP_EXAMPLES)
        assert 'Tcpdump Examples' in self.driver.title

    @pytest.mark.UI
    def test_what_is_api_button(self):
        self.main_page.go_out_from_visible_locator(self.main_page.locators.API_BUTTON)
        assert 'API - Wikipedia' in self.driver.title

    @pytest.mark.UI
    def test_future_of_internet_button(self):
        self.main_page.go_out_from_visible_locator(self.main_page.locators.FUTURE_OF_INTERNET)
        assert 'Future of internet' in self.driver.title

    @pytest.mark.UI
    def test_about_smtp_button(self):
        self.main_page.go_out_from_visible_locator(self.main_page.locators.SMTP)
        assert 'SMTP — Википедия' in self.driver.title

    @pytest.mark.UI
    def test_logout_button(self):
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        assert 'Welcome to the TEST SERVER' in self.authorization_page.driver.page_source

    @pytest.mark.UI
    def test_python_facts(self):
        self.main_page.find(self.main_page.locators.PYTHON_ZEN_QUOTE)

    @pytest.mark.UI
    def test_user_info(self):
        user_info = self.main_page.find(self.main_page.locators.LOGGED_AS).text
        assert user_info == f'Logged as {self.username}'

    @pytest.mark.UI
    def test_user_with_vk_id(self):
        with allure.step("Добавление VK ID пользователя для {username}..."):
            requests.post(f'http://0.0.0.0:9000/add_user/{self.username}')
        with allure.step('Получение VK ID пользователя {username}...'):
            response = requests.get(f'http://0.0.0.0:9000/vk_id/{self.username}').json()
        self.main_page.click(self.main_page.locators.HOME_BUTTON)
        self.main_page.find((By.XPATH, self.main_page.locators.VK_ID.format(response['vk_id'])))

    @pytest.mark.UI
    def test_user_without_vk_id(self):
        try:
            self.main_page.find(self.main_page.locators.VK_ID_NONE, 2)
        except TimeoutException:
            raise LocatorNotFoundError('Поле VK ID не пустое!')

    @pytest.mark.UI
    def test_activity_fields_in_db(self, mysql_client):
        user = mysql_client.select_by_username(self.username)
        assert user.active == 1
        assert user.start_active_time is not None

    @pytest.mark.UI
    def test_active_field_after_logout(self, mysql_client):
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON, 10)
        user = mysql_client.select_by_username(self.username)
        assert user.active == 0

    @pytest.mark.UI
    def test_deauthorization_after_blocking(self, fake_data, mysql_client):
        mysql_client.drop_access_by_username(username=fake_data['username'])
        self.main_page.click(self.main_page.locators.HOME_BUTTON)
        assert 'Welcome to the TEST SERVER' in self.authorization_page.driver.page_source

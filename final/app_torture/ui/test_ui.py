from datetime import datetime, timedelta

import allure
import pytest

from app_torture import base
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.reg_page import RegPage


class TestRegForm(base.BaseCase):

    @pytest.mark.UI
    @pytest.mark.parametrize("key, max",
                             [("name", 1), ("surname", 1), ("middle_name", 0), ("username", 6), ("email", 6),
                              ("password", 1)])
    def test_reg_pos(self, key, max, browser, mysql_delete):
        with allure.step("Entering registration page. Checking its open"):
            page = RegPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Entering valid data. Checking database and elements visibility"):
            page.do_register(data=self.fake_ui(key=key, max=max, valid=True))
            table = self.get_row(username=self.user_data["username"])
            assert table is not None, f"UserError: No such user {self.user_data['username']} in database."
            assert table["name"] == self.user_data[
                "name"], f"NameError: Expected:{self.user_data['name']}, Got: {table['name']}"
            assert table["surname"] == self.user_data[
                "surname"], f"SurnameError: Expected:{self.user_data['surname']}, Got: {table['surname']}"
            assert table["password"] == self.user_data[
                "password"], f"PasswordError: Expected:{self.user_data['password']}, Got: {table['password']}"
            assert table["email"] == self.user_data[
                "email"], f"EmailError: Expected:{self.user_data['email']}, Got: {table['email']}"
            assert table["access"] == 1, f"AccessValueError: Expected:1, Got: {table['access']}"
            assert MainPage(self.browser, timeout_to_open=10).is_open() is True

    @pytest.mark.UI
    def test_reg_fail(self, browser):
        with allure.step("Entering registration page. Checking its open"):
            page = RegPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Pressing register button without filling any field. Checking url and database"):
            self.fake_user(ui=True)
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Filling name field and pressing register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Filling name field, surname field and pressing register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Filling name, surname, login and pressing register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step("Filling name, surname, login, email and pressing register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step(
                "Filling name, surname, login, email, password and pressing register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step(
                "Filling name, surname, login, email, password and pressing checkbox and register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.click_checkbox()
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.is_open() is True
        with allure.step(
                "Filling name, surname, login, email, password, password_confirm and pressing checkbox and register button. Checking url and database"):
            page.input_name(self.user_data["name"])
            page.input_surname(self.user_data["surname"])
            page.input_username(self.user_data["username"])
            page.input_email(self.user_data["email"])
            page.input_password(self.user_data["password"])
            page.input_password_confirm(self.user_data["password"][:-1])
            page.click_checkbox()
            page.click_register()
            assert self.get_row(username=self.user_data["username"]) is None
            assert page.message() is True
            assert page.is_open() is True


class TestLoginForm(base.BaseCase):
    @pytest.mark.UI
    def test_login_fail(self, setup, add_to_mock, browser):
        with allure.step("Entering registration page. Checking its open"):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Login. Checking main page, elements and database"):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            assert page.vk_id_visible() is True
            row = self.get_row(username=setup["username"])
            assert row["active"] == 1
            current_time = datetime.now().replace(second=0, microsecond=0) - timedelta(hours=3)
            assert row["start_active_time"].replace(second=0, microsecond=0) == current_time
        with allure.step("Pressing logout, checking logout page and database"):
            page.click_logout()
            page = LoginPage(self.browser)
            assert page.is_open() is True
            assert self.get_row(username=setup["username"])["active"] == 0
            assert self.get_row(username=setup["username"])["access"] == 0

    @pytest.mark.UI
    def test_login(self, setup, browser):
        with allure.step("Entering registration page. Checking its open"):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Pressing auth button. Checking page url"):
            page.click_login()
            assert page.is_open() is True
        with allure.step("Filling login, pressing login button. Checking url"):
            page.input_username(setup["username"])
            page.click_login()
            assert page.is_open() is True
        with allure.step("Filling password, pressing login button. Checking url"):
            page.clear_username()
            page.input_password(setup["password"])
            page.click_login()
            assert page.is_open() is True
        with allure.step("Filling data switchly login = pass, pass = login. Pressing login button. Checking url"):
            page.clear_password()
            page.input_username(setup["password"])
            page.input_password(setup["username"])
            page.click_login()
            assert page.message() is True
            assert page.is_open() is True


class TestMainPage(base.BaseCase):

    @pytest.mark.UI
    def test_links(self, setup, browser):
        with allure.step("Entering login page. Checking its open"):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Auth. Checking page objects, vk_id, and all the links"):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            assert page.vk_id_visible() is False
            assert page.future_link_valid() is True
            assert page.smtp_link_valid() is True
            assert page.news_link_valid() is True
            assert page.download_link_valid() is True
            assert page.examples_link_valid() is True
            assert page.python_link_valid() is True
            assert page.python_history_link_valid() is True
            assert page.flask_link_valid() is True
            assert page.download_centos_link_valid() is True  # leads to fedora download
            assert page.api_link_valid() is True  # invalid

    @pytest.mark.UI
    def test_resolution(self, setup, browser):
        with allure.step("Entering login page. Checking its open"):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Auth. Checking element position and visibility due to heigth width"):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
            self.browser.set_window_size(width=1080, height=720)
            assert page.is_open() is True
            self.browser.set_window_size(width=800, height=600)
            assert page.is_open() is True
            self.browser.set_window_size(width=200, height=100)
            assert page.is_open() is True

    @pytest.mark.UI
    def test_access_auth(self, setup, browser):
        with allure.step("Entering login page. Checking its open"):
            page = LoginPage(self.browser).open()
            assert page.is_open() is True
        with allure.step("Auth. Checking page open"):
            page.do_login(data=setup)
            page = MainPage(self.browser)
            assert page.is_open() is True
        with allure.step("Changing access parametrs. Checking auth page opens"):
            self.mysql_update(user=setup["username"], field="access", value=2)
            assert self.get_row(username=setup["username"])["access"] == 2
            page.open()
            page = LoginPage(self.browser).open()
            assert page.is_open() is True

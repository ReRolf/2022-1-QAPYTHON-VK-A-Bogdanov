import allure
import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.authorization_page import AuthorizationPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage


class BaseCase:

    @pytest.fixture(scope='function')
    def setup(self, driver, config, ui_report, request: FixtureRequest):
        with allure.step("Первоначальная настройка для UI-тестов"):
            self.driver = driver
            self.config = config

            self.authorization_page: AuthorizationPage = request.getfixturevalue('authorization_page')
            self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')
            self.main_page: MainPage = request.getfixturevalue('main_page')

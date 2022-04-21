import os
import allure
import pytest
from base import BaseCase
from ui.locators import basic_locators


@allure.description(
    """These are negative tests on login"""
)
class TestNegative(BaseCase):
    def test_email(self):
        self.login_page.login('qwerty', 'password')
        assert self.login_page.find(basic_locators.FailureTests.EMAIL_LOGIN_FAILURE_LOCATOR)

    def test_password(self):
        self.login_page.login('valid_email@mail.ru', 'password')
        assert self.login_page.find(basic_locators.FailureTests.PASSWORD_LOGIN_FAILURE_LOCATOR)


@allure.description(
    """These are tests on campaign creation"""
)
class TestCampaign(BaseCase):
    @pytest.fixture()
    def file_path(self, repo_root):
        return os.path.join(repo_root, 'user_data', 'image.jpg')

    def test_campaign_create(self, credentials, file_path):
        self.login_page.login(*credentials)
        url = "https://taucetistation.org/"
        title = 'Space Station 13'
        age = '16-45'
        countries = 'Belarus'
        date_from = '21.04.2022'
        date_to = '22.04.2022'
        daily_budget = '100'
        total_budget = '200'
        self.campaign_page.campaign_create(url, title, age, countries, date_from, date_to, daily_budget, total_budget,
                                           file_path)
        self.campaign_page.check_campaign_detailed(url, title, age, countries, date_from, date_to, daily_budget,
                                                   total_budget)


@allure.description(
    """These are tests on segment creation"""
)
class TestSegment(BaseCase):
    def test_segment_create(self, credentials):
        self.login_page.login(*credentials)
        self.audience_page.segment_create()
        assert self.audience_page.find(self.audience_page.locators.SEGMENT_CREATED_LOCATOR)
        self.audience_page.segment_delete()

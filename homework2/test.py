import os
import allure
import pytest
from base import BaseCase
from ui.pages.login_page import LoginPage
from ui.pages.campaign_page import CampaignPage
from selenium.webdriver.common.by import By
from ui.pages.audience_page import AudiencePage
from ui.locators import basic_locators



@allure.description(
    """These are negative tests on login"""
)
class TestNegative(BaseCase):
    def test_email(self):
        login = LoginPage(self.driver)
        login.login('qwerty', 'password')
        assert login.find(basic_locators.FailureTests.EMAIL_LOGIN_FAILURE_LOCATOR)

    def test_password(self):
        login = LoginPage(self.driver)
        login.login('valid_email@mail.ru', 'password')
        assert login.find(basic_locators.FailureTests.PASSWORD_LOGIN_FAILURE_LOCATOR)


@allure.description(
    """These are tests on campaign creation"""
)
class TestCampaign(BaseCase):
    @pytest.fixture()
    def file_path(self, repo_root):
        return os.path.join(repo_root, 'user_data', 'image.jpg')

    def test_campaign_create(self, credentials, file_path):
        login = LoginPage(self.driver)
        login.login(*credentials)
        campaign = CampaignPage(self.driver)
        url = "https://taucetistation.org/"
        title = 'Space Station 13'
        age = '16-45'
        countries = 'Belarus'
        date_from = '21.04.2022'
        date_to = '22.04.2022'
        daily_budget = '100'
        total_budget = '200'
        campaign.campaign_create(url, title, age, countries, date_from, date_to, daily_budget, total_budget, file_path)
        campaign.campaign_create(url, title, age, countries, date_from, date_to, daily_budget, total_budget, file_path)
        campaign.check_campaign_detailed(url, title, age, countries, date_from, date_to, daily_budget, total_budget)


@allure.description(
    """These are tests on segment creation"""
)
class TestSegment(BaseCase):
    def test_segment_create(self, credentials):
        login = LoginPage(self.driver)
        login.login(*credentials)
        segment = AudiencePage(self.driver)
        segment.segment_create()
        assert segment.find(segment.locators.SEGMENT_CREATED_LOCATOR)
        segment = AudiencePage(self.driver)
        segment.segment_delete()

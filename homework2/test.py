import time

from base import BaseCase
from ui.pages.login_page import LoginPage
from ui.pages.campaign_page import CampaignPage
from selenium.webdriver.common.by import By
from ui.pages.audience_page import AudiencePage


class TestNegative(BaseCase):
    def test_email(self):
        login = LoginPage(self.driver)
        login.login('qwerty', 'password')
        assert self.driver.find_element(By.XPATH, "//div[contains(@class, 'notify-module-error')]")

    def test_password(self):
        login = LoginPage(self.driver)
        login.login('valid_email@mail.ru', 'password')
        assert self.driver.find_element(By.XPATH, "//div[@class = 'formMsg js_form_msg']")
        assert 'https://account.my.com/login/?error_code' in self.driver.current_url


class TestCampaign(BaseCase):
    def test_campaign_create(self):
        login = LoginPage(self.driver)
        login.login('bingodingo365@gmail.com', 'W9pale3K!')
        campaign = CampaignPage(self.driver)
        url = "https://taucetistation.org/"
        title = 'Space Station 13'
        age = '16-45'
        countries = 'Belarus'
        date_from = '21.04.2022'
        date_to = '22.04.2022'
        daily_budget = '100'
        total_budget = '200'
        photo_path = "/home/rolf/PycharmProject/project2/homework2/user_data/image.jpg"
        campaign.campaign_create(url, title, age, countries, date_from, date_to, daily_budget, total_budget, photo_path)
        campaign.check_campaign_detailed(url, title, age, countries, date_from, date_to, daily_budget, total_budget)


class TestSegment(BaseCase):
    def test_segment_create(self):
        login = LoginPage(self.driver)
        login.login('bingodingo365@gmail.com', 'W9pale3K!')
        segment = AudiencePage(self.driver)
        segment.segment_create()
        assert self.driver.find_element(By.XPATH,"//*[text() = 'SS13 segment']")

    def test_segment_delete(self):
        login = LoginPage(self.driver)
        login.login('bingodingo365@gmail.com', 'W9pale3K!')
        segment = AudiencePage(self.driver)
        segment.segment_delete()

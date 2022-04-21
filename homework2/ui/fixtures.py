import pytest
import allure
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.audience_page import AudiencePage
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@allure.title("driver creation")
@pytest.fixture()
def driver(config):
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)
    selenoid = config['selenoid']
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '98.0',
        }
    browser.get('https://target.my.com/')
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture
def audience_page(driver):
    return AudiencePage(driver=driver)

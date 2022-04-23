import os
import shutil
import sys
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ui.pages.audience_page import AudiencePage
from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.login_page import LoginPage


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@allure.title("driver creation")
@pytest.fixture()
def driver(config):
    selenoid = config['selenoid']
    options = Options()
    url = 'https://target.my.com/'
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            'version': '98.0',
        }
        driver = webdriver.Remote(
            'http://127.0.0.1:80/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    else:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.set_page_load_timeout(120)
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


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

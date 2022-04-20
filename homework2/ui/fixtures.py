import os

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
from pathlib import Path


@allure.title("driver creation")
@pytest.fixture()
def driver():
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)
    browser.get('https://target.my.com/')
    browser.maximize_window()
    yield browser
    browser.quit()


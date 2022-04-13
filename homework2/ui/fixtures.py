import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@allure.title("driver creation")
@pytest.fixture()
def driver():
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)
    browser.get('https://target.my.com/')
    browser.maximize_window()
    yield browser
    browser.quit()

@pytest.fixture(scope='session')
def credentials():
    with open('/home/rolf/PycharmProject/project2/homework2/user_data/logpass.txt', 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password
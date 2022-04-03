import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    browser = webdriver.Chrome(executable_path='/home/rolf/chromedriver')
    browser.maximize_window()
    yield browser
    browser.quit()

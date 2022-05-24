import os
import pytest
import allure

from selenium import webdriver

from ui.pages.authorization_page import AuthorizationPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage


@pytest.fixture(scope='function')
def driver(config):
    url = config['url']

    # capabilities = {
    #     "browserName": "chrome",
    #     "version": "95.0",
    # }
    options = webdriver.ChromeOptions()

    with allure.step("Подключение к браузеру через selenoid"):
        browser = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub",
                                   options=options)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def authorization_page(driver):
    return AuthorizationPage(driver=driver)


@pytest.fixture(scope='function')
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir):

    failed_tests_count = request.session.testsfailed

    yield

    if request.session.testsfailed > failed_tests_count:

        screenshot_file = os.path.join(test_dir, 'fail.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'fail.png',
                           attachment_type=allure.attachment_type.PNG)
        browser_logfile = os.path.join(test_dir, 'browser.log')

        with open(browser_logfile, 'w') as logfile:
            for i in driver.get_log('browser'):
                logfile.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as logfile:
            allure.attach(logfile.read(), 'browser.log',
                          attachment_type=allure.attachment_type.TEXT)

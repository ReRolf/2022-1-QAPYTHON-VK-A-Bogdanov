import time
import allure
from selenium.common.exceptions import ElementClickInterceptedException
from ui.locators import basic_locators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base import CustomError

CLICK_RETRY = 3


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):
    locators = basic_locators.BasePageLocators()
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 25
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Finding an element')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click')
    def click(self, *locators, timeout=None):
        for locator in locators:
            self.find(locator)
            element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
            for _ in range(CLICK_RETRY):
                try:
                    element.click()
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)

    @allure.step('Sending keys')
    def send_keys(self, locator, keys):
        self.find(locator).clear()
        self.find(locator).send_keys(keys)

    def checker_attribute(self, locator, result, attribute):
        element = self.find(locator)
        if element.get_attribute(attribute) == result:
            pass
        else:
            raise CustomError("Oops, something did not save")

    def checker_selector(self, locator, negative=False):
        if negative:
            element = self.find(locator)
            if not element.is_selected():
                pass
            else:
                raise CustomError("Oops, element did select")
        else:
            element = self.find(locator)
            if element.is_selected():
                pass
            else:
                raise CustomError("Oops, element did not select")

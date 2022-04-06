import pytest
from ui.locators import basic_locators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

CLICK_RETRY = 3


class BaseCase:
    driver = None
    wait = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver
        driver.get('https://target.my.com')
        self.wait = WebDriverWait(self.driver, 20)

    def find(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator))
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator)
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def login(self):
        email = "bingodingo365@gmail.com"
        password = "W9pale3K!"
        self.click(basic_locators.LOGIN_BUTTON_LOCATOR)
        self.find(basic_locators.QUERY_LOCATOR_EMAIL).send_keys(email)
        query_password = self.find(basic_locators.QUERY_LOCATOR_PASS)
        query_password.send_keys(password)
        query_password.send_keys(Keys.ENTER)
        self.find(basic_locators.SITE_IS_LOADED_LOCATOR)

    def logout(self):
        self.login()
        self.click(basic_locators.USER_BUTTON_LOCATOR)
        self.click(basic_locators.LOGOUT_BUTTON_LOCATOR)
        self.find(basic_locators.LOGIN_BUTTON_LOCATOR)

    def edit(self):
        self.login()
        self.click(basic_locators.PROFILE_BUTTON_LOCATOR)
        self.click(basic_locators.NAME_EDIT_LOCATOR)
        name = self.find(basic_locators.NAME_EDIT_LOCATOR)
        name.clear()
        name.send_keys("Andrew Bogdanov")
        phone = self.find(basic_locators.PHONE_EDIT_LOCATOR)
        phone.clear()
        phone.send_keys('89651961175')
        self.click(basic_locators.SAVE_BUTTON_LOCATOR)
        self.driver.refresh()
        self.click(basic_locators.SAVE_BUTTON_LOCATOR)
        name_edit = self.find(basic_locators.NAME_EDIT_LOCATOR)
        phone_edit = self.find(basic_locators.PHONE_EDIT_LOCATOR)
        if (name_edit.get_attribute('value') == "Andrew Bogdanov") and (
                phone_edit.get_attribute('value') == "89651961175"):
            return True

    def following(self, locator_button, locator):
        self.login()
        self.click(locator_button)
        self.find(locator)

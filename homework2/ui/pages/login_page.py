import allure
from ui.locators import basic_locators
from ui.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from ui.pages.dashboard_page import DashboardPage


class LoginPage(BasePage):
    locators = basic_locators.LoginPageLocators()

    @allure.step('Logging in')
    def login(self, user, password):
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)
        self.find(self.locators.QUERY_LOCATOR_EMAIL).send_keys(user)
        query_password = self.find(LoginPage.locators.QUERY_LOCATOR_PASS)
        query_password.send_keys(password)
        query_password.send_keys(Keys.ENTER)
        return DashboardPage(self.driver)

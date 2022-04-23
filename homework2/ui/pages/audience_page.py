import allure
from ui.locators import basic_locators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class AudiencePage(BasePage):
    locators = basic_locators.AudiencePageLocators()

    @allure.step('Creating a segment')
    def segment_create(self):
        dashboard_page = DashboardPage(self.driver)
        self.find(dashboard_page.locators.AUDIENCE_BUTTON_LOCATOR)
        self.click(dashboard_page.locators.AUDIENCE_BUTTON_LOCATOR)
        self.click(self.locators.CREATE_SEGMENT_LOCATOR, self.locators.CONTEXT_TARGETING_LOCATOR,
                   self.locators.SEGMENT_CHECKBOX_LOCATOR, self.locators.ADD_SEGMENT_LOCATOR)
        self.send_keys(self.locators.SEGMENT_NAME_LOCATOR, 'SS13 segment')
        self.click(self.locators.CREATE_SEGMENT_LOCATOR)
        self.find(self.locators.SITE_RELOADED_LOCATOR)

    @allure.step('Checking if segment creation was successful')
    def segment_delete(self):
        dashboard_page = DashboardPage(self.driver)
        self.click(dashboard_page.locators.AUDIENCE_BUTTON_LOCATOR)
        self.click(self.locators.DELETE_X_BUTTON_LOCATOR)
        self.click(self.locators.DELETE_SEGMENT_LOCATOR)

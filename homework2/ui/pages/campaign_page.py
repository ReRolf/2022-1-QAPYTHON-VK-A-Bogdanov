import allure
from ui.locators import basic_locators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class CampaignPage(BasePage):
    locators = basic_locators.CampaignPageLocators()

    @allure.step('Creating a campaign')
    def campaign_create(self, url, title, date_from, date_to, daily_budget,
                        total_budget, photo_path):
        try:
            self.click(DashboardPage.locators.CREATE_CAMPAIGN_HREF_LOCATOR)
        except Exception:
            pass
        try:
            self.click(DashboardPage.locators.CREATE_CAMPAIGN_BUTTON_LOCATOR)
        except Exception:
            pass
        self.click(self.locators.REACH_BUTTON_LOCATOR)
        self.send_keys(self.locators.CAMPAIGN_LINK_LOCATOR, url)
        self.click(self.locators.CLEAR_CAMPAIGN_NAME_LOCATOR)
        self.find(self.locators.CAMPAIGN_NAME_LOCATOR).send_keys(title)
        self.click(self.locators.TARGETING_BUTTON_LOCATOR)
        self.find(self.locators.TARGETING_CATEGORY_LOCATOR).send_keys('entertainment')
        self.find(self.locators.TARGETTING_TEXT_LOCATOR).send_keys('space station fun')
        self.click(self.locators.TARGETTING_CREATE_BUTTON_LOCATOR)
        self.click(self.locators.ACTIVE_CAMPAIGN_PERIOD_BUTTON_LOCATOR)
        self.send_keys(self.locators.PERIOD_DATE_FROM_TEXT_LOCATOR, date_from)
        self.send_keys(self.locators.PERIOD_DATE_TO_TEXT_LOCATOR, date_to)
        self.click(self.locators.CHANGE_STRATEGY_BUTTON_LOCATOR)
        self.send_keys(self.locators.DAILY_BUDGET_TEXT_LOCATOR, daily_budget)
        self.send_keys(self.locators.TOTAL_BUDGET_TEXT_LOCATOR, total_budget)
        self.click(self.locators.TEASER_BUTTON_LOCATOR)
        self.find(self.locators.UPLOAD_IMAGE_LOCATOR).send_keys(photo_path)
        self.click(self.locators.SAVE_IMAGE_LOCATOR)
        self.find(self.locators.AD_TITLE_TEXT_LOCATOR).send_keys(title)
        self.click(self.locators.SUMBIT_AD_LOCATOR)
        self.click(self.locators.CREATE_CAMPAIGN_LOCATOR)

    @allure.step('Checking if campaign creation was successful')
    def check_campaign_detailed(self, url, title, date_from, date_to, daily_budget, total_budget):
        self.find(DashboardPage.locators.PAGE_IS_LOADED_LOCATOR)
        self.checker_attribute(DashboardPage.locators.CAMPAIGN_NAME_LOCATOR, title, "title")
        self.click(DashboardPage.locators.CAMPAIGN_STATUS_LOCATOR, DashboardPage.locators.ACTIVE_CAMPAIGNS_LOCATOR,
                   DashboardPage.locators.CAMPAIGN_HREF_LOCATOR)
        p = self.driver.current_window_handle
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.find(self.locators.CREATE_CAMPAIGN_LOCATOR)
        self.checker_attribute(self.locators.CAMPAIGN_NAME_LOCATOR, title, "value")
        self.checker_attribute(self.locators.PERIOD_DATE_FROM_TEXT_LOCATOR, date_from, "value")
        self.checker_attribute(self.locators.PERIOD_DATE_TO_TEXT_LOCATOR, date_to, "value")
        self.checker_attribute(self.locators.DAILY_BUDGET_TEXT_LOCATOR, daily_budget, "value")
        self.checker_attribute(self.locators.TOTAL_BUDGET_TEXT_LOCATOR, total_budget, "value")
        self.checker_attribute(self.locators.URL_TEXT_LOCATOR, url, "defaultValue")

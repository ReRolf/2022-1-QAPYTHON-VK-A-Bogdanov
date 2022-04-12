from ui.locators import basic_locators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class CampaignPage(BasePage):
    locators = basic_locators.CampaignPageLocators()

    def campaign_create(self, url, title, age, countries, date_from, date_to, daily_budget,
                        total_budget, photo_path):
        self.click(DashboardPage.locators.CREATE_CAMPAIGN_BUTTON_LOCATOR, self.locators.REACH_BUTTON_LOCATOR)
        self.send_keys(self.locators.CAMPAIGN_LINK_LOCATOR, url)
        self.click(self.locators.CLEAR_CAMPAIGN_NAME_LOCATOR)
        self.find(self.locators.CAMPAIGN_NAME_LOCATOR).send_keys(title)
        self.click(self.locators.GENDER_BUTTON_LOCATOR, self.locators.NO_WOMAN_BUTTON_LOCATOR,
                   self.locators.AGE_BUTTON_LOCATOR, self.locators.SELECT_AGE_BUTTON_LOCATOR,
                   self.locators.CUSTOM_AGE_BUTTON_LOCATOR)
        self.send_keys(self.locators.TEXT_AGE_LOCATOR, age)
        self.send_keys(self.locators.ADD_COUNTRY_INPUT_LOCATOR, countries)
        self.click(self.locators.ADD_COUNTRY_BUTTON_LOCATOR, timeout=20)
        self.click(self.locators.SOCIAL_FEATURES_BUTTON_LOCATOR, self.locators.EDUCATION_FEATURE_LOCATOR,
                   self.locators.EDUCATION_CHECKBOX_LOCATOR, self.locators.INTERESTS_BUTTON_LOCATOR,
                   self.locators.CINEMA_INTERESTS_LOCATOR, self.locators.ADULT_CHECKBOX_LOCATOR,
                   self.locators.TARGETING_BUTTON_LOCATOR)
        self.find(self.locators.TARGETING_CATEGORY_LOCATOR).send_keys('entertainment')
        self.find(self.locators.TARGETTING_TEXT_LOCATOR).send_keys('space station fun')
        self.find(self.locators.TARGETTING_PERIOD_LOCATOR).send_keys('12d')
        self.click(self.locators.TARGETTING_CREATE_BUTTON_LOCATOR, self.locators.GROUPS_BUTTON_LOCATOR)
        self.send_keys(self.locators.NAME_GROUP_TEXT_LOCATOR, title)
        self.click(self.locators.DETAILED_SETUP_BUTTON, self.locators.AGE_RESTRICTION_BUTTON_LOCATOR,
                   self.locators.SELECT_RESTRICTION_BUTTON_LOCATOR, self.locators.AGE_RESTRICTION_16_LOCATOR,
                   self.locators.SPLIT_AUDIENCE_BUTTON_LOCATOR, self.locators.AUDIENCE_CHECKBOX_4_LOCATOR,
                   self.locators.DISPLAY_TIME_BUTTON_LOCATOR, self.locators.WEEKENDS_TIME_BUTTON_LOCATOR,
                   self.locators.WEEK_TIME_MONDAY_BUTTON_LOCATOR, self.locators.ACTIVE_CAMPAIGN_PERIOD_BUTTON_LOCATOR)
        self.send_keys(self.locators.PERIOD_DATE_FROM_TEXT_LOCATOR, date_from)
        self.send_keys(self.locators.PERIOD_DATE_TO_TEXT_LOCATOR, date_to)
        self.click(self.locators.CHANGE_STRATEGY_BUTTON_LOCATOR, self.locators.MIN_EXPENCE_CHECKBOX_LOCATOR)
        self.send_keys(self.locators.DAILY_BUDGET_TEXT_LOCATOR, daily_budget)
        self.send_keys(self.locators.TOTAL_BUDGET_TEXT_LOCATOR, total_budget)
        self.click(self.locators.TEASER_BUTTON_LOCATOR)
        self.find(self.locators.UPLOAD_IMAGE_LOCATOR).send_keys(photo_path)
        self.click(self.locators.SAVE_IMAGE_LOCATOR)
        self.find(self.locators.AD_TITLE_TEXT_LOCATOR).send_keys(title)
        self.find(self.locators.AD_TEXTAREA_LOCATOR).send_keys('The most autistic game')
        self.click(self.locators.SUMBIT_AD_LOCATOR)
        self.click(self.locators.CREATE_CAMPAIGN_LOCATOR)

    def check_campaign_detailed(self, url, title, age, country, date_from, date_to, daily_budget, total_budget):
        self.find(DashboardPage.locators.PAGE_IS_LOADED_LOCATOR)
        self.checker_attribute(DashboardPage.locators.CAMPAIGN_NAME_LOCATOR, title, "title")
        self.click(DashboardPage.locators.CAMPAIGN_STATUS_LOCATOR, DashboardPage.locators.ACTIVE_CAMPAIGNS_LOCATOR,
                   DashboardPage.locators.CAMPAIGN_HREF_LOCATOR)
        p = self.driver.current_window_handle
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.find(self.locators.CREATE_CAMPAIGN_LOCATOR)
        self.checker_attribute(self.locators.CAMPAIGN_NAME_LOCATOR, title, "value")
        self.checker_selector(self.locators.NO_WOMAN_BUTTON_LOCATOR, negative=True)
        self.click(self.locators.SELECT_AGE_BUTTON_LOCATOR, self.locators.CUSTOM_AGE_BUTTON_LOCATOR)
        self.checker_attribute(self.locators.TEXT_AGE_LOCATOR, age, "value")
        self.checker_attribute(self.locators.CREATED_REGION_LOCATOR, country, "textContent")
        self.click(self.locators.EDUCATION_FEATURE_LOCATOR)
        self.checker_selector(self.locators.EDUCATION_CHECKBOX_LOCATOR)
        self.click(self.locators.CINEMA_INTERESTS_LOCATOR)
        self.checker_selector(self.locators.ADULT_CHECKBOX_LOCATOR)
        self.checker_attribute(self.locators.SELECT_RESTRICTION_BUTTON_LOCATOR, "16+", "textContent")
        self.checker_selector(self.locators.AUDIENCE_CHECKBOX_4_LOCATOR, negative=True)
        self.checker_attribute(self.locators.PERIOD_DATE_FROM_TEXT_LOCATOR, date_from, "value")
        self.checker_attribute(self.locators.PERIOD_DATE_TO_TEXT_LOCATOR, date_to, "value")
        self.checker_attribute(self.locators.DAILY_BUDGET_TEXT_LOCATOR, daily_budget, "value")
        self.checker_attribute(self.locators.TOTAL_BUDGET_TEXT_LOCATOR, total_budget, "value")
        self.checker_attribute(self.locators.URL_TEXT_LOCATOR, url, "defaultValue")
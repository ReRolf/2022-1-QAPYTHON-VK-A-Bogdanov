from selenium.webdriver.common.by import By


class FailureTests:
    EMAIL_LOGIN_FAILURE_LOCATOR = (By.XPATH, "//div[contains(@class, 'notify-module-error')]")
    PASSWORD_LOGIN_FAILURE_LOCATOR = (By.XPATH, "//div[@class = 'formMsg js_form_msg']")


class LoginPageLocators:
    QUERY_LOCATOR_EMAIL = (By.NAME, 'email')
    QUERY_LOCATOR_PASS = (By.NAME, 'password')
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")


class BasePageLocators:
    USER_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
    PROFILE_BUTTON_LOCATOR = (By.XPATH, "//a[@data-gtm-id='pageview_profile']")
    TOOLS_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
    AUDIENCE_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-button') and @href = '/segments']")


class DashboardPageLocators(BasePageLocators):
    CREATE_CAMPAIGN_HREF_LOCATOR = (By.XPATH, "//a[@href='/campaign/new']")
    CREATE_CAMPAIGN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'dashboard-module-createButtonWrap')]/div")
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, "//a[@href = '/campaign/new']")
    PAGE_IS_LOADED_LOCATOR = (By.XPATH, "//div[@data-id='dragHandler']")
    CAMPAIGN_STATUS_LOCATOR = (By.XPATH, "//div[contains(@class, 'statusFilter')]/div")
    ACTIVE_CAMPAIGNS_LOCATOR = (By.XPATH, "//li[@data-id='0']")
    CAMPAIGN_HREF_LOCATOR = (By.XPATH, "//a[contains(@href, '/campaign')]")
    CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//a[contains(@class, 'nameCell-module-campaignNameLink')]")


class CampaignPageLocators(BasePageLocators):
    REACH_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, '_reach') and @data-class-name = 'ColumnListItemView']")
    CAMPAIGN_LINK_LOCATOR = (By.XPATH, "//input[@data-gtm-id='ad_url_text']")
    CLEAR_CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'js-input-clear')]")
    CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]/div/input")
    GENDER_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='sex']")
    NO_WOMAN_BUTTON_LOCATOR = (By.XPATH, "//li/input[contains(@id, 'female-view')]")
    AGE_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='age']")
    SELECT_AGE_BUTTON_LOCATOR = (
        By.XPATH, "//div[@data-class-name= 'SelectView']/div/div[contains(@class, 'select__item')]")
    CUSTOM_AGE_BUTTON_LOCATOR = (By.XPATH, "//li[@data-id = 'custom']")
    TEXT_AGE_LOCATOR = (By.XPATH, "//div[@class = 'textarea']/div/textarea")
    ADD_COUNTRY_INPUT_LOCATOR = (By.XPATH, "//div[contains(@class, 'region-module-selectors')]//input")
    ADD_COUNTRY_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'suggesterItemBtnAdd')]")
    SOCIAL_FEATURES_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='interests_soc_dem']")
    EDUCATION_FEATURE_LOCATOR = (By.XPATH, "//li[@data-id='10246']/span")
    EDUCATION_CHECKBOX_LOCATOR = (By.XPATH, "//input[@data-id='10247']")
    INTERESTS_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='interests']")
    CINEMA_INTERESTS_LOCATOR = (By.XPATH, "//li[@data-id='11825']/span")
    ADULT_CHECKBOX_LOCATOR = (By.XPATH, "//input[@data-id='11833']")
    TARGETING_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='context']")
    TARGETING_CATEGORY_LOCATOR = (By.XPATH, "//input[@data-test='productCategory']")
    TARGETTING_TEXT_LOCATOR = (By.XPATH, "//textarea[contains(@class, 'textareaNarrow')]")
    TARGETTING_PERIOD_LOCATOR = (By.XPATH, "//input[contains(@class, 'inputPeriod')]")
    TARGETTING_CREATE_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'contextForm-module-button')]")
    GROUPS_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='appsAndGroups']")
    NAME_GROUP_TEXT_LOCATOR = (By.XPATH, "//input[contains(@class, 'multiSelectSuggester')]")
    DETAILED_SETUP_BUTTON = (By.XPATH, "//div[@data-name='additionalTargeting']/div")
    AGE_RESTRICTION_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='age_restriction']")
    SELECT_RESTRICTION_BUTTON_LOCATOR = (
        By.XPATH, "//div[@class = 'select-module-select-39_icq' and @data-test='select']")
    AGE_RESTRICTION_16_LOCATOR = (By.XPATH, "//li[@data-id='16+']")
    SPLIT_AUDIENCE_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='split_audience']")
    AUDIENCE_CHECKBOX_4_LOCATOR = (
        By.XPATH, "//input[contains(@class,'splitAudience-module-checkbox') and @value = 4]/following-sibling::span")
    DISPLAY_TIME_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='fulltime']")
    WEEKENDS_TIME_BUTTON_LOCATOR = (By.XPATH, "//li[@data-name='weekends']")
    WEEK_TIME_MONDAY_BUTTON_LOCATOR = (
        By.XPATH, "//li[@data-id = '10' and contains(@class, 'full-time-setting__hour-cell')]")
    ACTIVE_CAMPAIGN_PERIOD_BUTTON_LOCATOR = (By.XPATH, "//div[@data-targeting='date']")
    PERIOD_DATE_FROM_TEXT_LOCATOR = (
        By.XPATH, "//div[@class = 'date-setting']/div[contains(@class, 'date-from')]/input")
    PERIOD_DATE_TO_TEXT_LOCATOR = (
        By.XPATH, "//div[@class = 'date-setting']/div[contains(@class, 'date-to')]/input")
    CHANGE_STRATEGY_BUTTON_LOCATOR = (By.XPATH, "//div[@data-class-name='Simple']/div/div")
    MIN_EXPENCE_CHECKBOX_LOCATOR = (By.XPATH, "//input[@value = 'second_price']")
    DAILY_BUDGET_TEXT_LOCATOR = (By.XPATH, "//input[@data-test='budget-per_day']")
    TOTAL_BUDGET_TEXT_LOCATOR = (By.XPATH, "//input[@data-test='budget-total']")
    TEASER_BUTTON_LOCATOR = (By.ID, 'patterns_teaser_57_58')
    UPLOAD_IMAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'roles-module-buttonWrap')]/div/input")
    SAVE_IMAGE_LOCATOR = (By.XPATH, "//input[@value='Save image']")
    AD_TITLE_TEXT_LOCATOR = (By.XPATH, "//input[@data-name='title_25']")
    AD_TEXTAREA_LOCATOR = (By.XPATH, "//textarea[@data-name='text_90']")
    SUMBIT_AD_LOCATOR = (By.XPATH, "//div[@data-test='submit_banner_button']")
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, "//div[contains(@class, 'footer__button')]/button[@data-class-name='Submit']")

    CREATED_REGION_LOCATOR = (By.XPATH, "//span[contains(@class, 'selectedRegions-module-regionName')]")
    URL_TEXT_LOCATOR = (By.XPATH, "//input[@data-name = 'primary']")


class AudiencePageLocators(BasePageLocators):
    CREATE_SEGMENT_LOCATOR = (By.XPATH, "//button[@data-class-name = 'Submit']")
    CONTEXT_TARGETING_LOCATOR = (By.XPATH, "//div[contains(@class, 'block-left')]/div[4]")
    SEGMENT_CHECKBOX_LOCATOR = (By.XPATH, "//div[contains(@class, 'sourcesList-module')]/div/div[1]/div[1]/input")
    ADD_SEGMENT_LOCATOR = (By.XPATH, "//div[contains(@class, 'adding-segments')]/button")
    SEGMENT_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]/div/input")
    SITE_RELOADED_LOCATOR = (By.XPATH, "//div[@class = 'segments-list']")
    DELETE_X_BUTTON_LOCATOR = (By.XPATH, "//span[contains(@class, 'icon-cross cells-module-removeCell')]")
    DELETE_SEGMENT_LOCATOR = (By.XPATH, "//button[@data-class-name='General']")
    SEGMENT_CREATED_LOCATOR = (By.XPATH, "//*[text() = 'SS13 segment']")

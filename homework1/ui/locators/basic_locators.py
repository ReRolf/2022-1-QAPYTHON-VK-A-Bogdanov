from selenium.webdriver.common.by import By

QUERY_LOCATOR_EMAIL = (By.NAME, 'email')
QUERY_LOCATOR_PASS = (By.NAME, 'password')
LOGIN_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
SITE_IS_LOADED_LOCATOR = (By.XPATH, "//div[contains(@class, 'instruction-module-title')]")

USER_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
LOGOUT_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'rightMenu-module-rightMenuLink') and @href = '/logout']")

PROFILE_BUTTON_LOCATOR = (By.XPATH, "//a[@data-gtm-id='pageview_profile']")
NAME_EDIT_LOCATOR = (By.XPATH, '//div[@data-name = "fio"]//input')
PHONE_EDIT_LOCATOR = (By.XPATH, '//div[@data-name = "phone"]//input')
SAVE_BUTTON_LOCATOR = (By.XPATH, '//div/*[@data-class-name = "Submit"]')

TOOLS_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
FEEDS_TITLE_LOCATOR = (By.XPATH, "//div[contains(@class, 'feeds-module-title')]")
AUDIENCE_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-button') and @href = '/segments']")
AUDIENCE_TEXT_LOCATOR = (By.XPATH, "//a[@href = '/segments/advertising_campaigns_list']")

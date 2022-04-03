from selenium.webdriver.common.by import By

QUERY_LOCATOR_EMAIL = (By.NAME, 'email')
QUERY_LOCATOR_PASS = (By.NAME, 'password')
LOGIN_BUTTON_LOCATOR = (By.XPATH, "//div[text()='Log in']")
SITE_IS_LOADED_LOCATOR = (By.XPATH, "//div[text()='How to get started?']")

USER_BUTTON_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
LOGOUT_BUTTON_LOCATOR = (By.XPATH, "//a[text()='Log off']")

PROFILE_BUTTON_LOCATOR = (By.XPATH, "//a[@data-gtm-id='pageview_profile']")
NAME_EDIT_LOCATOR = (By.XPATH, '//div[@data-name = "fio"]//input')
PHONE_EDIT_LOCATOR = (By.XPATH, '//div[@data-name = "phone"]//input')
SAVE_BUTTON_LOCATOR = (By.XPATH, '//div[text()="Save"]')

TOOLS_BUTTON_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-tools')]")
FEED_TEXT_LOCATOR = (By.XPATH, "//div[text()='Feeds list']")
AUDIENCE_BUTTON_LOCATOR = (By.XPATH, "//a[@href = '/segments']")
AUDIENCE_TEXT_LOCATOR = (By.XPATH, "//span[text()='Audience segments']")

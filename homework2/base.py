import os
import allure
import pytest
from _pytest.fixtures import FixtureRequest


class CustomError(Exception):
    pass


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.logger = logger
        self.config = config
        self.base_page: BasePage = (request.getfixturevalue('base_page'))
        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.audience_page: AudiencePage = (request.getfixturevalue('audience_page'))
        self.campaign_page: CampaignPage = (request.getfixturevalue('campaign_page'))

    # You should call this function only after clicking the button to open new window
    def switch_window(self, current, driver, close=False):
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        yield
        if close:
            driver.close()
        driver.switch_to.window(current)

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)

import pytest


class CustomError(Exception):
    pass


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, logger):
        self.driver = driver
        self.logger = logger

    # You should call this function only after clicking the button to open new window
    def switch_window(self, current, driver, close=False):
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        yield
        if close:
            driver.close()
        driver.switch_to.window(current)

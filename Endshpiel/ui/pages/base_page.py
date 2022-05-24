import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CLICK_RETRY = 3


class SecondTabError(Exception):
    pass


class LocatorNotFoundError(Exception):
    pass


class BasePage:
    locators = None

    def __init__(self, driver):
        self.driver = driver

    @allure.step('Клик {locator}')
    def click(self, locator, timeout=10):
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    @allure.step('Скролл {element}')
    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Поиск {locator}')
    def find(self, locator, timeout=10):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Передача <{message}> в локатор {locator}')
    def send_message(self, locator, message, timeout=10):
        field = self.wait(timeout).until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(message)

    @allure.step('Клик по спрятанному локатору {locator_hide}...')
    def click_on_hidden_element(self, locator_main, locator_hide):
        main = self.find(locator_main)
        hide = self.find(locator_hide)
        actions = ActionChains(self.driver)
        actions.move_to_element(main)
        actions.click(hide)
        actions.perform()

    @allure.step('Смена вкладки')
    def switch_to_second_tab(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
        except IndexError:
            raise SecondTabError('Новая вкладка не найдена')

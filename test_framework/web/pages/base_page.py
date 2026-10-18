from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def type(self, locator, text):
        self.find(locator).send_keys(text)

    def click(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator)).click()

    def get_text(self, locator):
        return self.find(locator).text

    def wait_text(self, locator, text):
        self.wait.until(ec.text_to_be_present_in_element(locator, text))
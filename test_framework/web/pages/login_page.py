from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import config

class LoginPage(BasePage):
    URL = config.BASE_URL + "/page/login"
    USERNAME = (By.ID, "username")
    PASSWORD = (By.CSS_SELECTOR,"#password")
    LOGIN_BTN = (By.XPATH, "//button[@id='login-btn']")
    RESULT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_result(self):
        return self.get_text(self.RESULT)
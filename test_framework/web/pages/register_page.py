from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import config

class RegisterPage(BasePage):
    URL = config.BASE_URL + "/page/register"
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    REGISTER_BTN = (By.ID, "register-btn")
    RESULT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def register(self, username, password, email, phone):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        self.click(self.REGISTER_BTN)

    def get_result(self):
        return self.get_text(self.RESULT)
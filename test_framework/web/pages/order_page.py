from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import config

class OrderPage(BasePage):
    URL = config.BASE_URL + "/page/my_orders"
    RESULT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def get_result(self):
        return self.get_text(self.RESULT)
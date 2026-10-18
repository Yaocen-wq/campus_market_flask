from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import config

class OrderSubmitPage(BasePage):
    URL = config.BASE_URL + "/page/order"
    PRODUCT_ID = (By.ID, "product_id")
    QUANTITY = (By.ID, "quantity")
    ORDER_BTN = (By.ID, "order-btn")
    RESULT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def order(self, product_id, quantity):
        self.type(self.PRODUCT_ID, product_id)
        self.type(self.QUANTITY, quantity)
        self.click(self.ORDER_BTN)

    def get_result(self):
        return self.get_text(self.RESULT)
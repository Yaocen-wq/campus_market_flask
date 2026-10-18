from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import config

class PublishPage(BasePage):
    URL = config.BASE_URL + "/page/publish"
    TITLE = (By.ID, "title")
    DESCRIPTION = (By.ID, "description")
    PRICE = (By.ID, "price")
    CATEGORY = (By.ID, "category")
    PUBLISH_BTN = (By.ID, "publish-btn")
    RESULT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def publish(self, title, description, price, category):
        self.type(self.TITLE, title)
        self.type(self.DESCRIPTION, description)
        self.type(self.PRICE, price)
        self.type(self.CATEGORY, category)
        self.click(self.PUBLISH_BTN)

    def get_result(self):
        return self.get_text(self.RESULT)
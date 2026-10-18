from pages.base_page import BasePage
import config

class HomePage(BasePage):
    URL = config.BASE_URL + "/"

    def open_page(self):
        self.open(self.URL)

    def get_title(self):
        return self.driver.title
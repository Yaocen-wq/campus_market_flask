from pages.login_page import LoginPage
from pages.order_page import OrderPage
import config

def test_order_po(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login(config.USER_1001, config.PASSWORD)

    order = OrderPage(driver)
    order.open_page()
    assert "请先登录" not in order.driver.page_source
from pages.login_page import LoginPage
from pages.order_page import OrderPage

def test_order_po(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login("huang_test_1001", "123456")

    order = OrderPage(driver)
    order.open_page()
    assert "请先登录" not in order.driver.page_source
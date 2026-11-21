from pages.login_page import LoginPage
from pages.order_page import OrderPage
from utils.data_loader import load_yaml

FIXTURES = load_yaml("fixtures.yaml")
OPERATOR = FIXTURES["accounts"]["web_operator"]
DATA = load_yaml("web/order.yaml")

def test_order_po(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login(OPERATOR["username"], OPERATOR["password"])

    order = OrderPage(driver)
    order.open_page()
    assert DATA["expected_absent_text"] not in order.driver.page_source

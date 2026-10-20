import pytest
from pages.login_page import LoginPage
from pages.order_submit_page import OrderSubmitPage
import config

@pytest.mark.parametrize(
    "quantity, expected_code, expected_msg",
    [
        pytest.param("0", "1", "数量不能为零", id="qty-0"),
        pytest.param("100", "1", "数量过多", id="qty-100"),
        pytest.param("-1", "1", "数量不能为负", id="qty-neg"),
    ],
)
def test_order_submit_po(driver, quantity, expected_code, expected_msg):
    login = LoginPage(driver)
    login.open_page()
    login.login(config.USER_1001, config.PASSWORD)

    page = OrderSubmitPage(driver)
    page.open_page()
    page.order(str(config.PRODUCT_ID), quantity)
    page.wait_text(OrderSubmitPage.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result
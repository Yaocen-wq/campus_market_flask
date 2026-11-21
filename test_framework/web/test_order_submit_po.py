import pytest
from pages.login_page import LoginPage
from pages.order_submit_page import OrderSubmitPage
from utils.data_loader import load_yaml

FIXTURES = load_yaml("fixtures.yaml")
OPERATOR = FIXTURES["accounts"]["web_operator"]
PRODUCT_ID = FIXTURES["products"]["order_target"]["product_id"]
RAW = load_yaml("web/order_submit.yaml")["cases"]


def _case(c):
    skip = c.get("skip")
    return pytest.param(c["quantity"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )

CASES = [_case(c) for c in RAW]

@pytest.mark.parametrize("quantity, expected_code, expected_msg", CASES)
def test_order_submit_po(driver, quantity, expected_code, expected_msg):
    login = LoginPage(driver)
    login.open_page()
    login.login(OPERATOR["username"], OPERATOR["password"])

    page = OrderSubmitPage(driver)
    page.open_page()
    page.order(str(PRODUCT_ID), quantity)
    page.wait_text(OrderSubmitPage.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result

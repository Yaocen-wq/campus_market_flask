import pytest
from pages.register_page import RegisterPage
from utils.data_loader import load_yaml

RAW = load_yaml("web/register.yaml")["cases"]

def _case(c):
    skip = c.get("skip")
    return pytest.param(c["username"], c["password"], c["email"], c["phone"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )

CASES = [_case(c) for c in RAW]

@pytest.mark.parametrize("username, password, email, phone, expected_code, expected_msg", CASES)
def test_register_po(driver, username, password, email, phone, expected_code, expected_msg):
    page = RegisterPage(driver)
    page.open_page()
    page.register(username, password, email, phone)
    page.wait_text(RegisterPage.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result

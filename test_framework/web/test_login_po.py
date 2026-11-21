import pytest
from pages.login_page import LoginPage
from utils.data_loader import load_yaml

RAW = load_yaml("web/login.yaml")["cases"]

def _cases(c):
    skip = c.get("skip")
    return pytest.param(c["username"], c["password"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )

CASES = [_cases(c) for c in RAW]

@pytest.mark.parametrize("username, password, code, msg",CASES)
def test_login_po(driver, username, password, code, msg):
    page = LoginPage(driver)
    page.open_page()
    page.login(username, password)
    page.wait_text(page.RESULT, "code=")
    result = page.get_result()
    assert msg in result
    assert f"code={code}" in result
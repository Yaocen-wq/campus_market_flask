import os
import pytest
import yaml
from pages.login_page import LoginPage
import config

DATA = os.path.join(config.ROOT_DIR, "data", "login.yaml")

with open(DATA, encoding="utf-8") as f:
    RAW = yaml.safe_load(f)["cases"]

def _case(c):
    skip = c.get("skip")
    return pytest.param(c["username"], c["password"], c["expected_code"], c["expected_msg"],
        id=c["id"],
        marks=pytest.mark.skip(reason=skip) if skip else ()
    )
CASES = [_case(c) for c in RAW]

@pytest.mark.parametrize("username, password, expected_code, expected_msg", CASES)
def test_login_po(driver, username, password, expected_code, expected_msg):
    page = LoginPage(driver)
    page.open_page()
    page.login(username, password)
    page.wait_text(page.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result

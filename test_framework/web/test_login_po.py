import pytest
from pages.login_page import LoginPage
import config
import random

@pytest.mark.parametrize(
    "username, password, expected_code",
    [
        pytest.param(config.USER_1003, "123456",       "0", id="login-1"),
        pytest.param("1003",           "wrong_pwd_999", "1", id="login-2"),
        pytest.param("not_exist_9527", "any_pwd_123",   "1", id="login-3"),
        pytest.param(" ", " ",   "1", id="login-4"),
    ]
)
def test_login_po(driver, username, password, expected_code):
    page = LoginPage(driver)
    page.open_page()
    page.login(username, password)
    page.wait_text(page.RESULT, "code=")
    assert f"code={expected_code}" in page.get_result()
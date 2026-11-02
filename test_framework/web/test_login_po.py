import pytest
from pages.login_page import LoginPage
import config

@pytest.mark.parametrize(
    "username, password, expected_code, expected_msg",
    [
        pytest.param(config.USER_1003, "123456", "0", "登录成功", id="login-1"),
        pytest.param(config.USER_1003, "wrong_pwd_999", "1", "密码错误", id="login-2"),
        pytest.param("not_exist_9527", "any_pwd_123", "1", "用户名不存在", id="login-3"),
        pytest.param(" ", " ", "1", "用户名不能为空", id="login-4"),
    ]
)
def test_login_po(driver, username, password, expected_code, expected_msg):
    page = LoginPage(driver)
    page.open_page()
    page.login(username, password)
    page.wait_text(page.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result
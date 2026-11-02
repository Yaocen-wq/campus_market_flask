import pytest
from pages.register_page import RegisterPage
import config

@pytest.mark.parametrize(
    "username, password, email, phone, expected_code, expected_msg",
    [
        pytest.param(config.REG_WEB["username"], config.REG_WEB["password"], config.REG_WEB["email"], config.REG_WEB["phone"], "0", "注册成功", id="reg-1"),
        pytest.param("huang_test_1005", "123456", "t1005@school.edu", "13800131005", "1", "注册失败", id="reg-2"),
        pytest.param(" ", " ", "t1005@school.edu", "13800131005", "1", "用户名不能为空", id="reg-3"),
    ],
)
def test_register_po(driver, username, password, email, phone, expected_code, expected_msg):
    page = RegisterPage(driver)
    page.open_page()
    page.register(username, password, email, phone)
    page.wait_text(RegisterPage.RESULT, "code=")
    result = page.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result
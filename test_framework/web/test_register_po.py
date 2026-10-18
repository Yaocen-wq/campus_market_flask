import pytest
from pages.register_page import RegisterPage
import config

@pytest.mark.parametrize(
    "username, password, email, phone, expected_code",
    [
        pytest.param(config.REG_WEB["username"], config.REG_WEB["password"], config.REG_WEB["email"], config.REG_WEB["phone"], "0", id="reg-1"),
        pytest.param("huang_test_1005", "123456", "t1005@school.edu", "13800131005", "1", id="reg-2"),
        pytest.param(" ", " ", "t1005@school.edu", "13800131005", "1", id="reg-3"),
    ],
)
def test_register_po(driver, username, password, email, phone, expected_code):
    page = RegisterPage(driver)
    page.open_page()
    page.register(username, password, email, phone)
    page.wait_text(RegisterPage.RESULT, "code=")
    assert f"code={expected_code}" in page.get_result()
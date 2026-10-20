from pages.login_page import LoginPage
from pages.publish_page import PublishPage
import pytest
import config

@pytest.mark.parametrize(
    "title, description, price, category, expected_code",
    [
        pytest.param("篮球", "九成新", "25", "体育器材", "0", id="pub-1"),
        pytest.param("", "九成新", "25", "体育器材", "1", id="pub-2"),
        pytest.param("篮球", "九成新", "100", "体育器材", "0", id="pub-3"),
        pytest.param("篮球", "", "25", "体育器材", "0", id="pub-4"),
        pytest.param("篮球", "", "0", "体育器材", "1", id="pub-5"),
        pytest.param("篮球", "", "-1", "体育器材", "1", id="pub-6"),
        pytest.param("篮球", "", "10000000", "体育器材", "1", id="pub-7"),
        pytest.param("篮球", "", "abc", "体育器材", "1", id="pub-8"),
    ],
)
def test_publish_po(driver, title, description, price, category, expected_code):
    login = LoginPage(driver)
    login.open_page()
    login.login(config.USER_1001, config.PASSWORD)

    pub = PublishPage(driver)
    pub.open_page()
    pub.publish(title, description, price, category)
    pub.wait_text(PublishPage.RESULT, "code=")
    assert f"code={expected_code}" in pub.get_result()
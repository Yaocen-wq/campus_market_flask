from pages.login_page import LoginPage
from pages.publish_page import PublishPage
import pytest
import config

@pytest.mark.parametrize(
    "title, description, price, category, expected_code, expected_msg",
    [
        pytest.param("篮球", "九成新", "25", "体育器材", "0", "发布成功",       id="pub-1"),
        pytest.param("", "九成新", "25", "体育器材", "1", "请输入商品名",   id="pub-2"),
        pytest.param("篮球", "九成新", "100", "体育器材", "0", "发布成功",       id="pub-3"),
        pytest.param("篮球", "", "25", "体育器材", "0", "发布成功",       id="pub-4"),
        pytest.param("篮球", "", "0", "体育器材", "1", "价格不能为零",   id="pub-5"),
        pytest.param("篮球", "", "-1", "体育器材", "1", "价格不能为负",   id="pub-6"),
        pytest.param("篮球", "", "10000000", "体育器材", "1", "价格过长",       id="pub-7"),
        pytest.param("篮球", "", "abc", "体育器材", "1", "请输入有效价格", id="pub-8"),
    ],
)
def test_publish_po(driver, title, description, price, category, expected_code, expected_msg):
    login = LoginPage(driver)
    login.open_page()
    login.login(config.USER_1001, config.PASSWORD)

    pub = PublishPage(driver)
    pub.open_page()
    pub.publish(title, description, price, category)
    pub.wait_text(PublishPage.RESULT, "code=")
    result = pub.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result
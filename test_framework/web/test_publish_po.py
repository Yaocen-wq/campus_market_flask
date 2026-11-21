import pytest
from pages.login_page import LoginPage
from pages.publish_page import PublishPage
from utils.data_loader import load_yaml

FIXTURES = load_yaml("fixtures.yaml")
OPERATOR = FIXTURES["accounts"]["web_operator"]
RAW = load_yaml("web/publish.yaml")["cases"]


def _case(c):
    skip = c.get("skip")
    return pytest.param(c["title"], c["description"], c["price"], c["category"],
                        c["expected_code"], c["expected_msg"], id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )

CASES = [_case(c) for c in RAW]

@pytest.mark.parametrize("title, description, price, category, expected_code, expected_msg", CASES)
def test_publish_po(driver, title, description, price, category, expected_code, expected_msg):
    login = LoginPage(driver)
    login.open_page()
    login.login(OPERATOR["username"], OPERATOR["password"])

    pub = PublishPage(driver)
    pub.open_page()
    pub.publish(title, description, price, category)
    pub.wait_text(PublishPage.RESULT, "code=")
    result = pub.get_result()
    assert f"code={expected_code}" in result
    assert expected_msg in result

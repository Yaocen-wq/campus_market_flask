import pytest, requests
from api_log import req
from utils.data_loader import load_yaml
import config

DATA = load_yaml("api/project.yaml")
FIXTURES = load_yaml("fixtures.yaml")
USER = DATA["user"]
PRODUCT_ID = FIXTURES["products"]["order_target"]["product_id"]
PRODUCT_PRICE = FIXTURES["products"]["order_target"]["price"]


@pytest.fixture
def login():
    s = requests.Session()
    r = req("POST", config.BASE_URL+"/login", session=s, data={"username": USER["username"], "password": USER["password"]})
    assert r.json()["code"] == 0, f"登录失败：{r.json()}"
    return s


def check(r, code, msg_kw):
    print(f"\n实际：code={r.json()['code']} msg={r.json()['msg']}")
    assert r.status_code == DATA["expect"]["status"]
    assert r.json()["code"] == code
    assert msg_kw in r.json()["msg"]


# ----- 注册 -----
def _register_case(c):
    skip = c.get("skip")
    return pytest.param(c["data"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )
REGISTER_CASES = [_register_case(c) for c in DATA["register_cases"]]

@pytest.mark.parametrize("data,code,msg_kw", REGISTER_CASES)
def test_register(data, code, msg_kw):
    check(req("POST", config.BASE_URL+"/register", data=data), code, msg_kw)


# ----- 登录 -----
def _login_case(c):
    skip = c.get("skip")
    return pytest.param(c["username"], c["password"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )
LOGIN_CASES = [_login_case(c) for c in DATA["login_cases"]]

@pytest.mark.parametrize("username,password,code,msg_kw", LOGIN_CASES)
def test_login(username, password, code, msg_kw):
    check(req("POST", config.BASE_URL+"/login", data={"username": username, "password": password}), code, msg_kw)


# ----- 发布 -----
def _publish_case(c):
    skip = c.get("skip")
    return pytest.param(c["data"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )
PUBLISH_CASES = [_publish_case(c) for c in DATA["publish_cases"]]

@pytest.mark.parametrize("data,code,msg_kw", PUBLISH_CASES)
def test_publish(login, data, code, msg_kw):
    check(req("POST", config.BASE_URL+"/publish_product", session=login, data=data), code, msg_kw)


# ----- 下单 -----
def _order_case(c):
    skip = c.get("skip")
    return pytest.param(c["quantity"], c["expected_code"], c["expected_msg"],
                        id=c["id"],
                        marks=pytest.mark.skip(reason=skip) if skip else ()
                        )
ORDER_CASES = [_order_case(c) for c in DATA["order_cases"]]

@pytest.mark.parametrize("quantity,code,msg_kw", ORDER_CASES)
def test_order(login, quantity, code, msg_kw):
    r = req("POST", config.BASE_URL+"/create_order", session=login, data={"product_id": PRODUCT_ID, "quantity": quantity})
    check(r, code, msg_kw)
    if code == 0:
        assert str(PRODUCT_PRICE * quantity) in r.json()["msg"]



def test_order_no_login():
    case = DATA["order_no_login"]
    check(req("POST", config.BASE_URL+"/create_order", data=case["payload"]), case["expected_code"], case["expected_msg"])


def test_mock_notify():
    case = DATA["mock_notify"]
    check(req("POST", config.MOCK_URL+"/pay/notify", data=case["payload"]), case["expected_code"], case["expected_msg"])


def test_orders(login):
    case = DATA["orders"]
    check(req("GET", config.BASE_URL+"/orders", session=login), case["expected_code"], case["expected_msg"])

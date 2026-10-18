import pytest
import requests
import config
from api_log import req

LOGIN_CASES = [
    pytest.param(config.USER_1015, config.PASSWORD, 0, "登录成功", id="登录-1015正例"),
    pytest.param(config.USER_1015, "000000", 1, "密码错误", id="登录-1015错密"),
    pytest.param("huang_test_9999", "123456", 1, "用户名不存在", id="登录-9999不存在"),
    pytest.param(config.USER_1015, "", 1, "不能为空", id="登录-不能为空"),
]

REGISTER_CASES = [
    pytest.param(config.REG_DDT, 0, "注册成功", id="注册-正例"),
    pytest.param({"username": config.USER_1015, "password": config.PASSWORD,
                  "email": "t1015@school.edu", "phone": "13800131015"},
                 1, "用户名已存在", id="注册-1015旧号反例"),
]

PUBLISH_CASES = [
    pytest.param(-1, 1, "不能为负", id="发布-负价拦截"),
    pytest.param(0, 1, "不能为零", id="发布-零价拦截"),
    pytest.param("abc", 1, "有效价格", id="发布-非数字拦截"),
    pytest.param(10000000, 1, "价格过长", id="发布-超上限拦截"),
    pytest.param(99, 0, "发布成功", id="发布-99放行造物"),
]

ORDER_CASES = [
    pytest.param(-1, 1, "不能为负", id="下单-数量负拦截"),
    pytest.param(0, 1, "不能为零", id="下单-数量零拦截"),
    pytest.param(100, 1, "数量过多", id="下单-数量超99拦截"),
]


def _login_1015():
    s = requests.Session()
    r = req("POST", f"{config.BASE_URL}/login", session=s,
            data={"username": config.USER_1015, "password": config.PASSWORD})
    assert r.json()["code"] == 0, f"登录失败：{r.json()}"
    return s


@pytest.mark.parametrize("username, password, code, msg_kw", LOGIN_CASES)
def test_login(username, password, code, msg_kw):
    r = req("POST", f"{config.BASE_URL}/login", data={"username": username, "password": password})
    body = r.json()
    print(f"\n实况：code={body['code']} msg={body['msg']}")
    assert r.status_code == 200
    assert body["code"] == code
    assert msg_kw in body["msg"]


@pytest.mark.parametrize("payload, code, msg_kw", REGISTER_CASES)
def test_register(payload, code, msg_kw):
    r = req("POST", f"{config.BASE_URL}/register", data=payload)
    body = r.json()
    print(f"\n实况：code={body['code']} msg={body['msg']}")
    assert r.status_code == 200
    assert body["code"] == code
    assert msg_kw in body["msg"]


@pytest.mark.parametrize("price, code, msg_kw", PUBLISH_CASES)
def test_publish(price, code, msg_kw):
    s = _login_1015()
    r = req("POST", f"{config.BASE_URL}/publish_product", session=s,
            data={"title": "PROBE_1009_阈值", "description": "数据驱动造物",
                  "price": price, "category": "其他"})
    body = r.json()
    print(f"\n实况：price={price} code={body['code']} msg={body['msg']}")
    assert r.status_code == 200
    assert body["code"] == code
    assert msg_kw in body["msg"]


@pytest.mark.parametrize("quantity, code, msg_kw", ORDER_CASES)
def test_create_order(quantity, code, msg_kw):
    s = _login_1015()
    r = req("GET", f"{config.BASE_URL}/products", session=s)
    assert r.status_code == 200 and r.json()["code"] == 0
    pid = r.json()["data"][0]["product_id"]
    r2 = req("POST", f"{config.BASE_URL}/create_order", session=s,
             data={"product_id": pid, "quantity": quantity})
    body = r2.json()
    print(f"\n实况：pid={pid} quantity={quantity} code={body['code']} msg={body['msg']}")
    assert r2.status_code == 200
    assert body["code"] == code
    assert msg_kw in body["msg"]
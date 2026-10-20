import pytest, requests
from api_log import req
import config

BASE = config.BASE_URL
MOCK = config.MOCK_URL
USER = config.REG_PROJECT
PUBLISH = {"title": "PROBE_1023_练习", "description": "描述", "price": 50, "category": "其他"}
PRODUCT_ID = config.PRODUCT_ID
PRODUCT_PRICE = config.PRODUCT_PRICE

@pytest.fixture
def login():
    s = requests.Session()
    r = req("POST", f"{BASE}/login", session=s, data={"username": USER["username"], "password": USER["password"]})
    assert r.json()["code"] == 0, f"登录失败：{r.json()}"
    return s

def check(r, code, msg_kw):
    print(f"\n实际：code={r.json()['code']} msg={r.json()['msg']}")
    assert r.status_code == 200
    assert r.json()["code"] == code
    assert msg_kw in r.json()["msg"]


# 注册
REGISTER_CASES = [
    pytest.param(USER, 0, "注册成功",id="正例"),
    pytest.param({**USER, "username": ""}, 1, "用户名不能为空",id="空用户名"),
    pytest.param({**USER, "username": "x"*17}, 1, "用户名过长",id="用户名过长"),
    pytest.param({**USER, "password": ""}, 1, "密码不能为空",id="空密码"),
    pytest.param(USER, 1, "已存在",id="重复"),
]
@pytest.mark.parametrize("data,code,msg_kw", REGISTER_CASES)
def test_register(data, code, msg_kw):
    check(req("POST", f"{BASE}/register", data=data), code, msg_kw)



# 登录
LOGIN_CASES = [
    pytest.param(USER["username"], USER["password"], 0, "登录成功",id="正例"),
    pytest.param("huang_test_9998", "123456", 1, "用户名不存在",id="假号"),
    pytest.param(USER["username"], "654321", 1, "密码错误",id="错密"),
    pytest.param(USER["username"], "", 1, "密码不能为空",id="空密码"),
]
@pytest.mark.parametrize("username,password,code,msg_kw", LOGIN_CASES)
def test_login(username, password, code, msg_kw):
    check(req("POST", f"{BASE}/login", data={"username": username, "password": password}), code, msg_kw)



# 发布
PUBLISH_CASES = [
    pytest.param({**PUBLISH, "title": "   "}, 1, "请输入商品名",id="空标题"),
    pytest.param({**PUBLISH, "title": "PROBE_1013_空描述", "description": ""}, 0, "发布成功",id="空描述过"),
    pytest.param({**PUBLISH, "price": 0}, 1, "价格不能为零",id="价格零"),
    pytest.param({**PUBLISH, "price": -1}, 1, "价格不能为负",id="价格负"),
    pytest.param({**PUBLISH, "price": 30.5}, 1, "请输入有效价格",id="小数"),
]
@pytest.mark.parametrize("data,code,msg_kw", PUBLISH_CASES)
def test_publish(login, data, code, msg_kw):
    check(req("POST", f"{BASE}/publish_product", session=login, data=data), code, msg_kw)



# ---------- 下单 4条 ----------
ORDER_CASES = [
    pytest.param(1, 0, "下单成功",id="正例"),
    pytest.param(0, 1, "数量不能为零",id="数量零"),
    pytest.param(100, 1, "数量过多",id="超99"),
]
@pytest.mark.parametrize("quantity,code,msg_kw", ORDER_CASES)
def test_order(login, quantity, code, msg_kw):
    r = req("POST", f"{BASE}/create_order", session=login,  data={"product_id": PRODUCT_ID, "quantity": quantity})
    check(r, code, msg_kw)
    if code == 0:
        assert str(PRODUCT_PRICE*quantity) in r.json()["msg"]

def test_order_no_login():# 未登录
    check(req("POST", f"{BASE}/create_order", data={"product_id": PRODUCT_ID, "quantity": 1}), 1, "请先登录！")



# ---------- 支付回调 1条（确保 mock_pay_server.py 在跑） ----------
def test_mock_notify():
    check(req("POST", f"{MOCK}/pay/notify",
              data={"order_id": "9999", "amount": "10.00", "trade_no": "MOCK001"}), 0, "成功")


# ---------- 订单 1条 ----------
def test_orders(login):
    check(req("GET", f"{BASE}/orders", session=login), 0, "查询成功")
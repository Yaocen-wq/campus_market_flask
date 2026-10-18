import pytest, requests
from api_log import req
import config

BASE = "http://127.0.0.1:5000"
MOCK = "http://127.0.0.1:5001"
USER = config.REG_PROJECT
PUBLISH = {"title": "PROBE_1023_练习", "description": "描述", "price": 50, "category": "其他"}
PRODUCT_ID = 101         # 商品id101
PRODUCT_PRICE = 99.0     # 价格99元

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
    (USER, 0, "注册成功"),
    ({**USER, "username": ""}, 1, "用户名不能为空"),
    ({**USER, "username": "x"*17}, 1, "用户名过长"),
    ({**USER, "password": ""}, 1, "密码不能为空"),
    (USER, 1, "已存在"),
]
@pytest.mark.parametrize("data,code,msg_kw", REGISTER_CASES, ids=["正例", "空用户名", "用户名过长", "空密码", "重复"])
def test_register(data, code, msg_kw):
    check(req("POST", f"{BASE}/register", data=data), code, msg_kw)



# 登录
LOGIN_CASES = [
    (USER["username"], USER["password"], 0, "登录成功"),
    ("huang_test_9998", "123456", 1, "用户名不存在"),
    (USER["username"], "654321", 1, "密码错误"),
    (USER["username"], "", 1, "密码不能为空"),
]
@pytest.mark.parametrize("username,password,code,msg_kw", LOGIN_CASES, ids=["正例", "假号", "错密密", "空密码"])
def test_login(username, password, code, msg_kw):
    check(req("POST", f"{BASE}/login", data={"username": username, "password": password}), code, msg_kw)



# 发布
PUBLISH_CASES = [
    ({**PUBLISH, "title": "   "}, 1, "请输入商品名"),
    ({**PUBLISH, "title": "PROBE_1013_空描述", "description": ""}, 0, "发布成功"),
    ({**PUBLISH, "price": 0}, 1, "价格不能为零"),
    ({**PUBLISH, "price": -1}, 1, "价格不能为负"),
    ({**PUBLISH, "price": 30.5}, 1, "请输入有效价格"),
]
@pytest.mark.parametrize("data,code,msg_kw", PUBLISH_CASES, ids=["空标题", "空描述放行", "价格零", "价格负", "小数"])
def test_publish(login, data, code, msg_kw):
    check(req("POST", f"{BASE}/publish_product", session=login, data=data), code, msg_kw)



# ---------- 下单 4条 ----------
ORDER_CASES = [
    (1, 0, "下单成功"),
    (0, 1, "数量不能为零"),
    (100, 1, "数量过多"),
]
@pytest.mark.parametrize("quantity,code,msg_kw", ORDER_CASES, ids=["正例", "数量零", "超99"])
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
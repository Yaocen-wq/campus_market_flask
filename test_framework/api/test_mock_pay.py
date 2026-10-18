import allure
from api_log import req

BASE = "http://127.0.0.1:5001"   # Mock支付服务

@allure.title("支付回调-正常")
@allure.description("期望 code=0 + msg含有成功")
def test_notify_ok():
    r = req("POST", f"{BASE}/pay/notify", data={"order_id": "9999", "amount": "10.00", "trade_no": "MOCK001"})
    print(f"\n实际：code={r.json()['code']} msg={r.json()['msg']}")
    assert r.status_code == 200
    assert r.json()["code"] == 0
    assert "成功" in r.json()["msg"]

@allure.title("支付回调-缺参")
@allure.description("期望 code=1 + msg ‘缺少参数：trade_no")
def test_notify_missing_param():
    r = req("POST", f"{BASE}/pay/notify", data={"order_id": "9999", "amount": "10.00"})
    body = r.json()
    print(f"\n实际：code={body['code']} msg={body['msg']}")
    assert r.status_code == 200
    assert body["code"] == 1
    assert "trade_no" in body["msg"]
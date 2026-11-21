import allure
import config
from api_log import req
from utils.data_loader import load_yaml

DATA = load_yaml("api/mock_pay.yaml")

@allure.title("支付回调-正常")
@allure.description(f"期望 code={DATA['notify_ok']['expected_code']} + msg 含 {DATA['notify_ok']['expected_msg']}")
def test_notify_ok():
    case = DATA["notify_ok"]
    r = req("POST", config.MOCK_URL+"/pay/notify", data=case["payload"])
    print(f"\n实际：code={r.json()['code']} msg={r.json()['msg']}")
    assert r.status_code == case["expected_status"]
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]


@allure.title("支付回调-缺参")
@allure.description(f"期望 code={DATA['notify_missing_param']['expected_code']} + msg 含 {DATA['notify_missing_param']['expected_msg']}")
def test_notify_missing_param():
    case = DATA["notify_missing_param"]
    r = req("POST", config.MOCK_URL+"/pay/notify", data=case["payload"])
    print(f"\n实际：code={r.json()['code']} msg={r.json()['msg']}")
    assert r.status_code == case["expected_status"]
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]

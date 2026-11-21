from api_log import req
from utils.data_loader import load_yaml
import config

DATA = load_yaml("api/negative.yaml")


def test_publish_without_login():
    case = DATA["publish_without_login"]
    r = req("POST", config.BASE_URL + "/publish_product", data=case["payload"])
    print("未登录发布：", r.json()["msg"])
    assert r.status_code == case["expected_status"]
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]


def test_order_without_login():
    case = DATA["order_without_login"]
    r = req("POST", config.BASE_URL + "/create_order", data=case["payload"])
    print("未登录下单：", r.json()["msg"])
    assert r.status_code == case["expected_status"]
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]


def test_register_duplicate():
    case = DATA["register_duplicate"]
    r = req("POST", config.BASE_URL + "/register", data=case["payload"])
    print("重复注册：", r.json()["msg"])
    assert r.status_code == case["expected_status"]
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]

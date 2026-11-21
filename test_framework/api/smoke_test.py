from api_log import req
from utils.data_loader import load_yaml
import config

DATA = load_yaml("api/smoke.yaml")

def test_home_status():
    r = req("GET", config.BASE_URL + "/")
    print("首页状态码:", r.status_code)
    assert r.status_code == DATA["home"]["expected_status"]

def test_login_fake_user():
    case = DATA["login_fake"]
    r = req("POST", config.BASE_URL + "/login", data=case["payload"])
    assert r.status_code == case["expected_status"]
    print("假号msg:", r.json()["msg"])
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]

def test_login_real_user():
    case = DATA["login_real"]
    r = req("POST", config.BASE_URL + "/login", data=case["payload"])
    assert r.status_code == case["expected_status"]
    print("真号msg:", r.json()["msg"])
    assert r.json()["code"] == case["expected_code"]
    assert case["expected_msg"] in r.json()["msg"]

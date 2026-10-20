from api_log import req
import config

def test_home_status():
    r = req("GET", config.BASE_URL + "/")
    print("首页状态码:", r.status_code)
    assert r.status_code == 200

def test_login_fake_user():
    r = req("POST", config.BASE_URL + "/login", data={"username": "huang_test_9999", "password": "123456"})
    assert r.status_code == 200
    print("假号msg:", r.json()["msg"])
    assert r.json()["code"] == 1
    assert "用户名不存在" in r.json()["msg"]

def test_login_real_user():
    r = req("POST", config.BASE_URL + "/login", data={"username": config.USER_1003, "password": config.PASSWORD})
    assert r.status_code == 200
    print("真号msg:", r.json()["msg"])
    assert r.json()["code"] == 0
    assert "登录成功" in r.json()["msg"]
import requests
import config
from api_log import req
from utils.data_loader import load_yaml

DATA = load_yaml("api/chain.yaml")
USER = DATA["user"]
EXPECT = DATA["expect"]


def test_full_chain():
    s = requests.Session()
    # 注册
    r = req("POST", config.BASE_URL + "/register", session=s, data=USER)
    assert r.status_code == EXPECT["status_ok"]
    assert r.json()["code"] == EXPECT["code_ok"]
    assert EXPECT["register_msg"] in r.json()["msg"]
    print("注册：", r.json()["msg"])

    # 登录
    r = req("POST", config.BASE_URL + "/login", session=s, data={
        "username": USER["username"],
        "password": USER["password"],
    })
    assert r.status_code == EXPECT["status_ok"]
    assert r.json()["code"] == EXPECT["code_ok"]
    assert EXPECT["login_msg"] in r.json()["msg"]
    print("登录：", r.json()["msg"])

    # 发布
    r = req("POST", config.BASE_URL + "/publish_product", session=s, data=DATA["publish"])
    assert r.status_code == EXPECT["status_ok"]
    assert r.json()["code"] == EXPECT["code_ok"]
    assert EXPECT["publish_msg"] in r.json()["msg"]
    print("发布：", r.json()["msg"])

    # 取id
    r = req("GET", config.BASE_URL + "/products", session=s)
    assert r.status_code == EXPECT["status_ok"]
    assert r.json()["code"] == EXPECT["code_ok"]
    product_id = r.json()["data"][0]["product_id"]
    print("取id：", product_id)

    # 下单
    r = req("POST", config.BASE_URL + "/create_order", session=s, data={
        "product_id": product_id,
        "quantity": DATA["order"]["quantity"],
    })
    assert r.status_code == EXPECT["status_ok"]
    assert r.json()["code"] == EXPECT["code_ok"]
    assert EXPECT["order_msg"] in r.json()["msg"]
    print("下单：", r.json()["msg"])

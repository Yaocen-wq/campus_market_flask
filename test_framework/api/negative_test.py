import requests
import config

def test_publish_without_login():
    r = requests.post(config.BASE_URL+"/publish_product",data={
        "title":"未登录商品",
        "price":"40",
        "description":"未登录测试",
        "category":"其他",
    })
    print("未登录发布：",r.json()["msg"])
    assert r.status_code == 200
    assert r.json()["code"] == 1
    assert "请先登录" in r.json()["msg"]


def test_order_without_login():
    r = requests.post(config.BASE_URL+"/create_order",data={
        "product_id":"95",
        "quantity":"1",
    })
    print("未登录下单：",r.json()["msg"])
    assert r.status_code == 200
    assert r.json()["code"] == 1
    assert "请先登录" in r.json()["msg"]


def test_register_duplicate():
    r = requests.post(config.BASE_URL+"/register",data={
        "username":config.USER_1015,
        "password":config.PASSWORD,
        "email":"t1015@school.edu",
        "phone":"13800131015",
    })
    print("重复注册：",r.json()["msg"])
    assert r.status_code == 200
    assert r.json()["code"] == 1
    assert "用户名已存在" in r.json()["msg"]
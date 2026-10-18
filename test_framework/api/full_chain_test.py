import requests
import config

def test_full_chain():
    s = requests.Session()
    # 注册
    r = s.post(config.BASE_URL+"/register",data=config.REG_CHAIN)
    assert r.status_code == 200
    assert r.json()["code"] == 0
    assert "注册成功" in r.json()["msg"]
    print("注册：",r.json()["msg"])


    # 登录
    r = s.post(config.BASE_URL+"/login",data={
        "username":config.USER_1015,
        "password":config.PASSWORD
    })
    assert r.status_code == 200
    assert r.json()["code"] == 0
    assert "登录成功" in r.json()["msg"]
    print("登录：",r.json()["msg"])


    # 发布
    r = s.post(config.BASE_URL+"/publish_product",data={
        "title":"测试商品",
        "price":"40",
        "description":"测试用",
        "category":"其他"
    })
    assert r.status_code == 200
    assert r.json()["code"] == 0
    assert "发布成功" in r.json()["msg"]
    print("发布：",r.json()["msg"])


    # 取id
    r = s.get(config.BASE_URL + "/products")
    assert r.status_code == 200
    assert r.json()["code"] == 0
    product_id = r.json()["data"][0]["product_id"]
    print("取id：", product_id)


    # 下单
    r = s.post(config.BASE_URL+"/create_order",data={
        "product_id":product_id,
        "quantity":"1"
    })
    assert r.json()["code"] == 0
    assert r.status_code == 200
    assert "下单成功" in r.json()["msg"]
    print("下单：",r.json()["msg"])
import requests
import config
BASE = config.BASE_URL

r = requests.post(BASE+"/login",data={
    "username":config.USER_1015,
    "password":config.PASSWORD,
})

msg = r.json()["msg"]
uid = msg.split("：")[-1]
ids = {uid}

print("msg原文：",msg)
print("刮出的ID：",uid)

assert "126" in ids
print("核对通过：126在集合里")
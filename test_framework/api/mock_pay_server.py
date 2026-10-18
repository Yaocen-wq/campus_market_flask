from flask import Flask, request, jsonify

app = Flask("mock_pay") 

@app.route("/pay/notify", methods=["POST"])
def pay_notify():
    order_id = request.form.get("order_id")
    amount = request.form.get("amount")
    trade_no = request.form.get("trade_no")

    if order_id is None or order_id.strip() == "":
        return jsonify({"code": 1, "msg": "缺少参数：order_id"})
    if amount is None or amount.strip() == "":
        return jsonify({"code": 1, "msg": "缺少参数：amount"})
    if trade_no is None or trade_no.strip() == "":
        return jsonify({"code": 1, "msg": "缺少参数：trade_no"})
    if order_id == "FAIL":
        return jsonify({"code": 1, "msg": "支付失败：余额不足"})

    return jsonify({"code": 0, "msg": "支付回调成功", "order_id": order_id, "trade_no": trade_no})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
import os
import pymysql
from flask import Flask, request, jsonify, session, render_template

app = Flask("campus_market")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "campus_flea_market")


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/page/register")
def register_page():
    return render_template("register.html")


@app.route("/page/login")
def login_page():
    return render_template("login.html")


@app.route("/page/publish")
def publish_page():
    return render_template("publish.html")


@app.route("/page/order")
def order_page():
    return render_template("order.html")


@app.route("/page/my_orders")
def my_orders_page():
    return render_template("my_orders.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if username is None or username.strip() == "":
        return jsonify({"code": 1, "msg": "用户名不能为空"})

    elif len(username) > 16:

        return jsonify({"code": 1, "msg": "用户名过长"})

    elif password is None or password == "":

        return jsonify({"code": 1, "msg": "密码不能为空"})

    elif len(password) > 16:

        return jsonify({"code": 1, "msg": "密码过长"})

    elif email is None or email == "":

        return jsonify({"code": 1, "msg": "邮箱不能为空"})

    elif phone is None or phone == "":

        return jsonify({"code": 1, "msg": "手机号不能为空"})

    conn = get_conn()

    cursor = conn.cursor()
    sql = "INSERT INTO users (username,password,email,phone) VALUES (%s, %s, %s, %s);"
    data = (username, password, email, phone)

    try:
        cursor.execute(sql, data)
        conn.commit()
        return jsonify({"code": 0, "msg": "注册成功"})
    except pymysql.err.IntegrityError as e:
        error_msg = str(e)
        if "email" in error_msg:
            return jsonify({"code": 1, "msg": "注册失败：邮箱已存在"})
        elif "username" in error_msg:
            return jsonify({"code": 1, "msg": "注册失败：用户名已存在"})
        else:
            return jsonify({"code": 1, "msg": "注册失败：字段已存在"})
    except Exception as e:
        return jsonify({"code": 1, "msg": "注册失败：" + str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username is None or username.strip() == "":
        return jsonify({"code": 1, "msg": "用户名不能为空"})

    if password is None or password == "":
        return jsonify({"code": 1, "msg": "密码不能为空"})

    conn = get_conn()

    cursor = conn.cursor()
    sql = "SELECT user_id, password FROM users WHERE username = %s;"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return jsonify({"code": 1, "msg": "用户名不存在"})

    if password != result[1]:
        return jsonify({"code": 1, "msg": "密码错误"})

    session["user_id"] = result[0]
    return jsonify({"code": 0, "msg": "登录成功 用户ID：" + str(result[0])})


@app.route("/publish_product", methods=["POST"])
def publish_product():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"code": 1, "msg": "请先登录！"})

    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    category = request.form.get("category")

    if title is None or title.strip() == "":
        return jsonify({"code": 1, "msg": "请输入商品名"})

    if len(title) > 20:
        return jsonify({"code": 1, "msg": "商品名过长"})

    if price == "":
        return jsonify({"code": 1, "msg": "价格不能为空"})

    try:
        price_num = float(price)
    except Exception:

        return jsonify({"code": 1, "msg": "请输入有效价格"})

    if price_num >= 10000000:
        return jsonify({"code": 1, "msg": "价格过长"})

    if price_num < 0:
        return jsonify({"code": 1, "msg": "价格不能为负"})

    if price_num == 0:
        return jsonify({"code": 1, "msg": "价格不能为零"})

    if not price.isdigit():
        return jsonify({"code": 1, "msg": "请输入有效价格"})
    conn = get_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO products (seller_id, title, description, price, category) VALUES (%s, %s, %s, %s, %s);"

    try:
        cursor.execute(sql, (user_id, title, description, price, category))
        conn.commit()
        return jsonify({"code": 0, "msg": "发布成功"})
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 1, "msg": "发布失败：" + str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route("/create_order", methods=["POST"])
def create_order():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"code": 1, "msg": "请先登录！"})

    product_id = request.form.get("product_id")
    conn = get_conn()
    cursor = conn.cursor()

    try:
        sql_product = "SELECT seller_id, price, status, title FROM products WHERE product_id = %s;"
        cursor.execute(sql_product, (product_id,))
        product = cursor.fetchone()

        if product is None:
            return jsonify({"code": 1, "msg": "商品不存在"})
        seller_id, price, status, title = product

        if status != 1:
            return jsonify({"code": 1, "msg": "该商品已下架，无法购买"})
        quantity = int(request.form.get("quantity"))

        if quantity < 0:
            return jsonify({"code": 1, "msg": "数量不能为负"})

        if quantity == 0:
            return jsonify({"code": 1, "msg": "数量不能为零"})

        if quantity > 99:
            return jsonify({"code": 1, "msg": "数量过多"})

        total_price = float(price) * quantity
        sql_order = "INSERT INTO orders (buyer_id, product_id, seller_id, quantity, total_price) VALUES (%s, %s, %s, %s, %s);"

        cursor.execute(sql_order, (user_id, product_id, seller_id, quantity, total_price))
        conn.commit()

        return jsonify({"code": 0, "msg": "下单成功 金额：" + str(total_price) + "元"})
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 1, "msg": "下单失败"})
    finally:
        cursor.close()
        conn.close()


@app.route("/products", methods=["GET"])
def get_products():
    conn = get_conn()
    cursor = conn.cursor()
    sql = "SELECT product_id, title, price, category FROM products WHERE status = 1 ORDER BY product_id DESC;"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    product_list = []
    for row in rows:
        product_list.append({"product_id": row[0], "title": row[1], "price": float(row[2]), "category": row[3]})

    return jsonify({"code": 0, "msg": "查询成功", "data": product_list})


@app.route("/orders", methods=["GET"])
def get_orders():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"code": 1, "msg": "请先登录！"})

    conn = get_conn()
    cursor = conn.cursor()
    sql = "SELECT o.order_id, p.title, o.quantity, o.total_price, o.created_at FROM orders o JOIN products p ON o.product_id = p.product_id WHERE o.buyer_id = %s ORDER BY o.created_at DESC;"
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    order_list = []
    for row in rows:
        order_list.append({"order_id": row[0], "title": row[1], "quantity": row[2], "total_price": float(row[3]), "created_at": str(row[4])})

    return jsonify({"code": 0, "msg": "查询成功", "data": order_list})


app.run(debug=True)
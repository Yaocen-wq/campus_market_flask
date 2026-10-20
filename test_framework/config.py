import os

ROOT_DIR    = os.path.dirname(os.path.abspath(__file__))          # test_framework
LOG_DIR     = os.path.join(ROOT_DIR, "logs")                      # 日志
SHOT_DIR    = os.path.join(ROOT_DIR, "web", "screenshots")        # 失败截图
ALLURE_DIR  = os.path.join(ROOT_DIR, "allure-results")            # 报告

# 地址
BASE_URL = "http://127.0.0.1:5000"   # 被测平台
MOCK_URL = "http://127.0.0.1:5001"   # 支付Mock

# ── 账号：一处改、全局生效 ──
PASSWORD = "123456"
USER_1001 = "huang_test_1001"   # Web：登录/下单/发布
USER_1003 = "huang_test_1003"   # Web 登录正例；接口冒烟真号
USER_1005 = "huang_test_1005"   # Web 重复注册反例
USER_1015 = "huang_test_1015"   # 接口锚点/DDT；uid 必须=126

# 重跑前换成没用过的号
REG_DDT     = {"username": "huang_test_1038", "password": "123456", "email": "t1038@school.edu", "phone": "13800131038"}  # ddt_test
REG_CHAIN   = {"username": "huang_test_1039", "password": "123456", "email": "t1039@school.edu", "phone": "13800131039"}  # full_chain_test
REG_PROJECT = {"username": "huang_test_1036", "password": "123456", "email": "t1036@school.edu", "phone": "13800131036"}  # project_test 20条
REG_WEB     = {"username": "huang_test_1037", "password": "123456", "email": "t1037@school.edu", "phone": "13800131037"}  # test_register_po

# 商品id和价格
PRODUCT_ID    = 101
PRODUCT_PRICE = 99.0
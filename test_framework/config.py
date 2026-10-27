import os

# 路径
ROOT_DIR    = os.path.dirname(os.path.abspath(__file__))          # test_framework绝对路径
LOG_DIR     = os.path.join(ROOT_DIR, "logs")                      # 日志
SHOT_DIR    = os.path.join(ROOT_DIR, "web", "screenshots")        # 失败截图
ALLURE_DIR  = os.path.join(ROOT_DIR, "allure-results")            # 报告

# 地址
BASE_URL = "http://127.0.0.1:5000"   # 被测平台
MOCK_URL = "http://127.0.0.1:5001"   # 支付Mock

# 账号
PASSWORD = "123456"
USER_1001 = "huang_test_1001"   # Web登录后下单/发布
USER_1003 = "huang_test_1003"   # Web登录正例/接口冒烟
USER_1005 = "huang_test_1005"   # Web重复注册反例
USER_1015 = "huang_test_1015"   # 接口锚点 uid=4


REG_CHAIN   = {"username": "huang_test_1040", "password": "123456", "email": "t1040@school.edu", "phone": "13800131040"}  # full_chain_test
REG_PROJECT = {"username": "huang_test_1036", "password": "123456", "email": "t1036@school.edu", "phone": "13800131036"}  # project_test 20条
REG_WEB     = {"username": "huang_test_1037", "password": "123456", "email": "t1037@school.edu", "phone": "13800131037"}  # test_register_po

# 商品id和价格
PRODUCT_ID    = 101
PRODUCT_PRICE = 99.0
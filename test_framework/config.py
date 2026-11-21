import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   #test_framework 的绝对路径
DATA_DIR = os.path.join(ROOT_DIR, "data")               # 数据文件的路径
LOG_DIR = os.path.join(ROOT_DIR, "logs")                # 日志目录
SHOT_DIR = os.path.join(ROOT_DIR, "web", "screenshots") # 失败截图目录
ALLURE_DIR = os.path.join(ROOT_DIR, "allure-results")   # Allure 原始结果目录

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000") # 被测平台地址
MOCK_URL = os.environ.get("MOCK_URL", "http://127.0.0.1:5001") # Mock 地址

WAIT_TIMEOUT = 10 # web 模块显式等待页面最大秒数

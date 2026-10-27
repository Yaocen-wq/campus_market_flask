import os
import datetime
import pytest
import allure
from selenium import webdriver
import config
from utils.logger import get_logger

log = get_logger("frame")

@pytest.fixture(scope="session")
def driver():
    d = webdriver.Edge()
    d.maximize_window()
    yield d
    d.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 剔除不符合的
    if report.when not in ("setup", "call") or not report.failed:
        return
    try:
        d = item.funcargs.get("driver")
        if d is None:
            return

    # 路径+名字
        os.makedirs(config.SHOT_DIR, exist_ok=True)
        date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        err = "fail"
        crash = getattr(report.longrepr, "reprcrash", None)
        if crash is not None:
            err = crash.message.split(":")[0].strip()
        shot = os.path.join(config.SHOT_DIR, f"{date}_{item.name}_{err}.png")

    # 保存+allure报告
        d.save_screenshot(shot)
        allure.attach.file(shot, name=os.path.basename(shot),attachment_type=allure.attachment_type.PNG)
        log.info(f"SHOT {item.name} -> {shot}")
    except Exception as e:
        log.info(f"SHOT-FAIL {item.name}: {e}")
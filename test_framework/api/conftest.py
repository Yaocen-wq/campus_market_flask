import allure
import pytest
import api_log
from utils.logger import get_logger

log = get_logger("api")

@pytest.fixture(autouse=True)
def _fresh_records():
    api_log.clear_records()
    yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    try:
        if not api_log.RECORDS:
            return
        text = f"用例：{item.name}\n结果：{report.outcome}\n\n" + "\n\n".join(api_log.RECORDS)
        allure.attach(text, name=f"接口证据_{item.name}",attachment_type=allure.attachment_type.TEXT)
        log.info(f"EVIDENCE {item.name} -> {len(api_log.RECORDS)} 条")
    except Exception as e:
        log.info(f"EVIDENCE-FAIL {item.name}: {e}")
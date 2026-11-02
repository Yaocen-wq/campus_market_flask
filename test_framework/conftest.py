from utils.logger import get_logger
import pytest
import fail_report

log = get_logger("root")

def pytest_runtest_logreport(report):
    if report.when == "call":
        log.info(f"{report.outcome.upper()} {report.nodeid}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed and call.excinfo is not None:
        report.exc_name = call.excinfo.type.__name__

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    fail_report.make_summary(terminalreporter)
from utils.logger import get_logger      # 路径锚：导入本文件 = test_framework 进 sys.path

log = get_logger("root")


def pytest_runtest_logreport(report):
    if report.when == "call":
        log.info(f"{report.outcome.upper()} {report.nodeid}")
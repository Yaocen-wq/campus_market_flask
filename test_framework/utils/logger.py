import os
import logging
import config

LOG_FILE = os.path.join(config.LOG_DIR, "test.log")

def get_logger(name="test"):

    os.makedirs(config.LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(fh)
    return logger
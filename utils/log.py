import os
import logging
from utils.utilities import env_or_default

LOG_FILE = "test_log.log"

def logging_config():
    # set default log level to INFO
    log_level = env_or_default("LOG_LEVEL", "INFO").upper()

    # validate log level string corresponding to logging level constant
    numeric_level = getattr(logging, log_level, None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    handler = logging.FileHandler(LOG_FILE, mode="w")
    logger.addHandler(handler)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(
        f"Logging configured with log level: {log_level}"
    )
    return logger

logger = logging_config()

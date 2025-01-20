import logging
from settings import config


__all__ = ["setup_logger", "get_log_format"]


def get_log_format() -> str:
    return "%(asctime)s - %(levelname)s - %(message)s"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(config.app.SLUG)
    console_handler = logging.StreamHandler()

    if config.app.DEBUG is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter(get_log_format())
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

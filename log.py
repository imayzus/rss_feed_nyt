import os
import logging


DEFAULT_FORMAT = "[%(levelname)s] %(asctime)s : ProcessID: %(process)d : " "%(filename)s %(funcName)s Message: %(message)s"
LOGGERS = {}


def _get_logger(name, fmt, added_filter=None):
    logger = logging.getLogger(name)
    logger.propagate = False
    if added_filter:
        logger.addFilter(added_filter)
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(fmt)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
    return logger


def get_logger(name, log_level=None, fmt=DEFAULT_FORMAT, added_filter=None):
    log_level = log_level or os.environ.get("LOGLEVEL", "INFO").upper()
    if name not in LOGGERS:
        LOGGERS[name] = _get_logger(name, fmt, added_filter)
    logger = LOGGERS[name]
    logger.setLevel(log_level)
    return logger


def default_logger(name):
    logger = get_logger(name, fmt=DEFAULT_FORMAT)
    logger.setLevel(logging.DEBUG)
    logger.disabled = False
    return logger

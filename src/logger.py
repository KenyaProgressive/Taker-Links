import sys
from loguru import logger
from const import LOG_FORMAT

def logger_setup():

    logger.remove()

    logger.add(
        sys.stderr,
        format=LOG_FORMAT,
        backtrace=True,
        diagnose=False,
    )
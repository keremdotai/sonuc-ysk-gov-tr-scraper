import logging
from pathlib import Path
import sys
import traceback


__all__ = [
    'create_logger',
    'log_exception',
]


logging.basicConfig(
    filename=str(Path(__file__).parent.parent / 'log'),
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    level=logging.INFO,
    )


def create_logger():
    return logging.getLogger('')


def log_exception(logger, e):
    logger.error(f"EXCEPTION: {repr(e)}")

    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)

    logger.error(f"- Exception type: {ex_type.__name__}")
    logger.error(f"- Exception message: {ex_value}")
    logger.error(f"- Stack trace:")
    for i, trace in enumerate(trace_back):
        logger.error(f"{'-' * (i + 2)} In {trace[0]}, line {trace[1]}, in function {trace[2]}: '{trace[3]}'")

import sys
from loguru import logger
from loguru._logger import Logger


def get_logger(log_file_path: str) -> Logger:
    format = '{time} [{level}] {message}'
    logger.remove()
    logger.add(
        sink=log_file_path,
        format=format,
        rotation="1 MB",
        level='INFO',
    )
    logger.add(
        sink=sys.stdout,
        format=format,
    )
    return logger

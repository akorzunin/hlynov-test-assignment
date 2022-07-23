import sys
from loguru import logger
def get_logger(log_file_path):
    format='{time} [{level}] {message}'
    logger.remove()
    logger.add(
        sink=log_file_path,
        format=format,
    )
    logger.add(
        sink=sys.stdout,
        format=format
    )
    return logger
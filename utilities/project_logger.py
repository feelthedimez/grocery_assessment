import logging
from .path_finder import get_path_to_file

def get_file_handler() -> logging.FileHandler:
    """Set up the logger for files"""

    logger_file = get_path_to_file('logs', 'automation.log')
    logger_file_format = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(filename=logger_file)
    file_handler.setFormatter(fmt=logger_file_format)
    return file_handler


def get_logger(logger_name=__name__):
    """Setu up the logger, adding levels and handlers"""

    user_logger = logging.getLogger(logger_name)
    user_logger.setLevel(logging.DEBUG)
    user_logger.addHandler(get_file_handler())
    user_logger.propagate = False

    return user_logger

import logging
from logging import Logger
from colorlog import ColoredFormatter

def configure_logging(level=logging.DEBUG):
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    def create_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logger.addHandler(handler)
            logger.setLevel(level)
        return logger

    return create_logger

create_logger = configure_logging()
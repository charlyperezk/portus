import sys
import logging
from logging import Logger
from colorlog import ColoredFormatter
from loguru import logger as loguru_logger

# Setup loguru (for file logging, structured logging, etc.)
def setup_loguru():
    loguru_logger.remove()

    loguru_logger.add(sys.stdout, level="DEBUG", colorize=True)

    loguru_logger.add(
        "logs/app.log",
        rotation="1 week",
        level="DEBUG",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = loguru_logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            loguru_logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


    root_logger = logging.getLogger()
    root_logger.handlers = [InterceptHandler()]
    root_logger.setLevel(logging.DEBUG)

    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)

    # Intercept uvicorn logs
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging_logger = logging.getLogger(name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = True

# Colored developer-friendly logger
def configure_colored_logger(level=logging.DEBUG):
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s:%(name)s:%(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'SUCCESS': 'bold_green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    def create_logger(name: str) -> Logger:
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logger.addHandler(handler)
            logger.setLevel(level)
        return logger

    return create_logger

create_logger = configure_colored_logger()
setup_loguru()
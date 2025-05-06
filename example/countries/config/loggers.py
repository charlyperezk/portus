import logging
from src.common.logger import configure_logging

SERVICE_NAME = "CountryCRUDService"
create_logger = configure_logging(logging.DEBUG)
loggers = {
    "service": create_logger(SERVICE_NAME),
    "repository": create_logger(f"{SERVICE_NAME}:Repository"),
}

service_logger = loggers["service"]
repository_logger = loggers["repository"]
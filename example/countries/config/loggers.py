import logging
from src.portus.common.logger import configure_colored_logger

SERVICE_NAME = "CountryCRUDService"
create_logger = configure_colored_logger(logging.INFO)
loggers = {
    "service": create_logger(SERVICE_NAME),
    "repository": create_logger(f"{SERVICE_NAME}:Repository"),
}

service_logger = loggers["service"]
repository_logger = loggers["repository"]
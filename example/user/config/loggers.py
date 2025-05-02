import logging
from src.common.logger import configure_logging

SERVICE_NAME = "UserService"
create_logger = configure_logging(logging.DEBUG)
loggers = {
    "service": create_logger(SERVICE_NAME),
    "orchestrator": create_logger(f"{SERVICE_NAME}:HooksOrchestrator"),
    "notifications": create_logger(f"{SERVICE_NAME}:MailService")
}

service_logger = loggers["service"]
orchestrator_logger = loggers["orchestrator"]
notifications_logger = loggers["notifications"]
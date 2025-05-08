import logging
from src.portus.common.logger import configure_colored_logger

SERVICE_NAME = "UserService"
create_logger = configure_colored_logger(logging.INFO)
loggers = {
    "service": create_logger(SERVICE_NAME),
    "orchestrator": create_logger(f"{SERVICE_NAME}:HooksOrchestrator"),
    "notifications": create_logger(f"{SERVICE_NAME}:MailService"),
    "repository": create_logger(f"{SERVICE_NAME}:Repository"),
    "related_repository": create_logger(f"{SERVICE_NAME}:RelatedRepository"),
}

service_logger = loggers["service"]
orchestrator_logger = loggers["orchestrator"]
notifications_logger = loggers["notifications"]
repository_logger = loggers["repository"]
related_repository_logger = loggers["related_repository"]
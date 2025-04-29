from common.types import TInternalData
from hooks.logger import LogCompositorHook
from logging import Logger

def make_entity_created_logger(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"{entity_name.capitalize()} created with ID {data.get_value('id')}"
    return LogCompositorHook(logger, log_fn)

def make_entity_updated_logger(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"{entity_name.capitalize()} updated with ID {data.get_value('id')}"
    return LogCompositorHook(logger, log_fn)

def make_welcome_email_sent_logger(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"Welcome email sent to {entity_name.capitalize()} with Email {data.get_value('email')}"
    return LogCompositorHook(logger, log_fn)

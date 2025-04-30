from common.types import TInternalData
from hooks.logger import LogCompositorHook
from logging import Logger

def make_entity_created_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"{entity_name.capitalize()} created with ID {data.get_value('id')}"
    return LogCompositorHook(logger, log_fn)

def make_entity_updated_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"{entity_name.capitalize()} updated with ID {data.get_value('id')}"
    return LogCompositorHook(logger, log_fn)

def make_entity_deleted_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"{entity_name.capitalize()} deleted with ID {data.get_value('id')}"
    return LogCompositorHook(logger, log_fn)

def make_welcome_email_sent_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"Welcome email sent to {entity_name.capitalize()} with Email {data.get_value('email')}"
    return LogCompositorHook(logger, log_fn)

def make_update_email_sent_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"Data updated email sent to {entity_name.capitalize()} with Email {data.get_value('email')}"
    return LogCompositorHook(logger, log_fn)

def make_deletion_email_sent_log(logger: Logger, entity_name: str) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"Account deleted email sent to {entity_name.capitalize()} with Email {data.get_value('email')}"
    return LogCompositorHook(logger, log_fn)

def make_internal_data_trace_log(logger: Logger) -> LogCompositorHook:
    def log_fn(data: TInternalData) -> str:
        return f"InternalData trace {tuple(enumerate(data.trace))}"
    return LogCompositorHook(logger, log_fn)
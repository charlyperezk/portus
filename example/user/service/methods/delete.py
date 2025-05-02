from src.common.types import PASSIVE_DELETION_FLAG
from src.adapters.output.notifications import NotificationPort, Notifications
from src.utils.functions import add_timestamps
from src.hooks.transformer import make_static_fields_hook, make_context_flag_hook
from src.hooks.triggerer import make_email_notification_trigger_hook

from example.user.config import notifications_logger, delete_email

def delete_transformation_hooks():
    return [
        make_context_flag_hook(PASSIVE_DELETION_FLAG),
        make_static_fields_hook({'active': False}),
        make_static_fields_hook(add_timestamps(["updated_at"]))
    ]

def delete_trigger_hooks(notifications_service: NotificationPort=Notifications(notifications_logger)):
    return [
        make_email_notification_trigger_hook(
            notification_service=notifications_service,
            **delete_email
        )
    ]
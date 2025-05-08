from src.portus.common.types import PASSIVE_DELETION_FLAG
from src.portus.adapters.output.notifications import NotificationPort, Notifications
from src.portus.utils.functions import add_timestamps
from src.portus.hooks.transformer import static_fields_hook, context_flag_hook
from src.portus.hooks.triggerer import email_notification_trigger_hook

from example.user.config import notifications_logger, delete_email

def delete_transformation_hooks():
    return [
        # context_flag_hook(PASSIVE_DELETION_FLAG),
        # static_fields_hook({'active': False}),
        # static_fields_hook(add_timestamps(["updated_at"]))
    ]

def delete_trigger_hooks(notifications_service: NotificationPort=Notifications(notifications_logger)):
    return [
        email_notification_trigger_hook(
            notification_service=notifications_service,
            **delete_email
        )
    ]
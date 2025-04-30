import logging
from common.types import PASIVE_DELETION_FLAG
from adapters.output.notifications import NotificationPort, Notifications
from utils.functions import add_timestamps
from hooks.transformer import make_static_fields_hook, make_context_static_field_hook
from hooks.triggerer import make_email_notification_trigger_hook
from hooks.logger import make_deletion_email_sent_log, make_entity_deleted_log

logger = logging.getLogger(__name__)

def get_delete_transformation_hooks():
    return [
        make_context_static_field_hook({PASIVE_DELETION_FLAG: True}),
        make_static_fields_hook({'active': False}),
        make_static_fields_hook(add_timestamps(["updated_at"]))
    ]

def get_delete_trigger_hooks(notifications_service: NotificationPort=Notifications()):
    return [
        make_entity_deleted_log(logger, "User"),
        make_email_notification_trigger_hook(
            notification_service=notifications_service,
            subject="Your account was deleted succesfully.",
            body="This is an example email"
        ),
        make_deletion_email_sent_log(logger, "User")
    ]
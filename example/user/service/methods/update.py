from src.adapters.output.notifications import NotificationPort, Notifications
from src.utils.functions import add_timestamps
from src.hooks.relation.setter import relation_context_hook
from src.hooks.relation.validator import relation_exists_hook
from src.hooks.transformer import static_fields_hook
from src.hooks.validator import check_unique_email_hook
from src.hooks.triggerer import email_notification_trigger_hook

from example.user.config import notifications_logger, update_email

def update_validation_hooks(
    user_repository,
    country_repository
):
    return [
        check_unique_email_hook("email", user_repository),
        relation_exists_hook("country_id", country_repository)
    ]

def update_transformation_hooks(country_repository):
    return [
        relation_context_hook("country_id", country_repository),
        static_fields_hook(add_timestamps(["updated_at"]))
    ]

def update_trigger_hooks(notifications_service: NotificationPort=Notifications(notifications_logger)):
    return [
        email_notification_trigger_hook(
        notification_service=notifications_service,
        **update_email
        )
    ]
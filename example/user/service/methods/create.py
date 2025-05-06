from example.user.config import notifications_logger, user_defaults, create_email
from src.adapters.output.notifications import NotificationPort, Notifications
from src.utils.functions import add_id, add_timestamps, hash_password
from src.hooks.relation.setter import relation_context_hook
from src.hooks.relation.validator import relation_exists_hook
from src.hooks.transformer import static_fields_hook, hash_field_hook
from src.hooks.validator import check_unique_email_hook
from src.hooks.triggerer import email_notification_trigger_hook

def create_validation_hooks(
    user_repository,
    country_repository
):
    return [
        check_unique_email_hook("email", user_repository),
        relation_exists_hook("country_id", country_repository)
    ]

def create_transformation_hooks(country_repository):
    return [
        hash_field_hook("password", hash_password),
        relation_context_hook("country_id", country_repository),
        static_fields_hook(user_defaults),
        static_fields_hook(add_id("id")),
        static_fields_hook(add_timestamps(["created_at", "updated_at"]))
    ]

def create_trigger_hooks(notifications_service: NotificationPort=Notifications(notifications_logger)):
    return [
        email_notification_trigger_hook(
            notification_service=notifications_service,
            **create_email
        )
    ]
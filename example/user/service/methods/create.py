from example.user.config import notifications_logger, user_defaults, create_email
from example.user.repositories import CountryRelationRepository, UserInMemoryRepository
from src.adapters.output.notifications import NotificationPort, Notifications
from src.utils.functions import add_id, add_timestamps, hash_password
from src.hooks.relation.setter import make_relation_context_hook
from src.hooks.relation.validator import make_relation_exists_hook
from src.hooks.transformer import make_static_fields_hook, make_hash_field_hook
from src.hooks.validator import make_check_unique_email_hook
from src.hooks.triggerer import make_email_notification_trigger_hook

def create_validation_hooks(
    user_repository: UserInMemoryRepository,
    country_repository: CountryRelationRepository
):
    return [
        make_check_unique_email_hook("email", user_repository),
        make_relation_exists_hook("country_id", country_repository)
    ]

def create_transformation_hooks(country_repository: CountryRelationRepository):
    return [
        make_hash_field_hook("password", hash_password),
        make_relation_context_hook("country_id", country_repository),
        make_static_fields_hook(user_defaults),
        make_static_fields_hook(add_id("id")),
        make_static_fields_hook(add_timestamps(["created_at", "updated_at"]))
    ]

def create_trigger_hooks(notifications_service: NotificationPort=Notifications(notifications_logger)):
    return [
        make_email_notification_trigger_hook(
            notification_service=notifications_service,
            **create_email
        )
    ]
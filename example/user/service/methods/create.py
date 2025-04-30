import logging
from example.user.repositories import CountryRelationRepository, UserInMemoryRepository
from adapters.output.notifications import NotificationPort, Notifications
from utils.functions import add_id, add_timestamps, hash_password
from hooks.relation.setter import make_relation_context_hook
from hooks.relation.validator import make_relation_exists_hook
from hooks.transformer import make_static_fields_hook, make_hash_field_hook
from hooks.validator import make_check_unique_email_hook
from hooks.triggerer import make_email_notification_trigger_hook
from hooks.logger import make_welcome_email_sent_log, make_entity_created_log

logger = logging.getLogger(__name__)

def add_default_config():
    return {
        "role": "standard",
        "active": True,
        "verified": False
    }

def get_create_validation_hooks(
    user_repository: UserInMemoryRepository,
    country_repository: CountryRelationRepository
):
    return [
        make_check_unique_email_hook("email", user_repository),
        make_relation_exists_hook("country_id", country_repository)
    ]

def get_create_transformation_hooks(country_repository: CountryRelationRepository):
    return [
        make_hash_field_hook("password", hash_password),
        make_relation_context_hook("country_id", country_repository),
        make_static_fields_hook(add_default_config()),
        make_static_fields_hook(add_id("id")),
        make_static_fields_hook(add_timestamps(["created_at", "updated_at"]))
    ]

def get_create_trigger_hooks(notifications_service: NotificationPort=Notifications()):
    return [
        make_entity_created_log(logger, "User"),
        make_email_notification_trigger_hook(
            notification_service=notifications_service,
            subject="¡Welcome from Portus Service!",
            body="This is an example email"
        ),
        make_welcome_email_sent_log(logger, "User")    
    ]
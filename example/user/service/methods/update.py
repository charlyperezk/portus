from hooks.base import CompositeHook, ValidateAndTransformComposite, LifeCycle
from hooks.triggers import EmitEventHook
from hooks.core.setters import ComputedFieldsHook
from hooks.core.validators import RelationExistsHook
from hooks.functions import set_update_time, send_update_email
from example.user.repositories.country_repository import CountryRelationRepository

before_transformations = [
    ComputedFieldsHook(set_update_time),

]

before_validations = [
    RelationExistsHook(CountryRelationRepository(), "country_id")
]

after_triggers = [
    EmitEventHook("UserUpdated", lambda data: print(f"[Event:UserUpdated] User updated successfully. (ID {data.id})")),
    EmitEventHook("UserUpdated", send_update_email)
]

update_life_cycle = LifeCycle(
    before=ValidateAndTransformComposite(
        validations=CompositeHook(before_validations),
        transformations=CompositeHook(before_transformations)
    ),
    after=CompositeHook(after_triggers)
)
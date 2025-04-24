from hooks.base import AsyncCompositeHook, ValidateAndTransformComposite, LifeCycle, ParallelCompositeHook
from hooks.triggers import EmitEventHook
from hooks.core.setters import ComputedFieldsHook
from hooks.core.validators import RelationExistsHook
from hooks.functions import set_update_time, send_update_email
from example.user.repositories.country_repository import CountryRelationRepository

before_validations = [
    RelationExistsHook(CountryRelationRepository(), "country_id")
]

before_transformations = [
    ComputedFieldsHook(set_update_time),

]

after_triggers = [
    EmitEventHook("UserUpdated", lambda data: print(f"[Event:UserUpdated] User updated successfully. (ID {data.id})")),
    EmitEventHook("UserUpdated", send_update_email)
]

update_life_cycle = LifeCycle(
    before=ValidateAndTransformComposite(
        validations=ParallelCompositeHook(before_validations),
        transformations=AsyncCompositeHook(before_transformations)
    ),
    after=ParallelCompositeHook(after_triggers)
)
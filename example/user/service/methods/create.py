from hooks.base import AsyncCompositeHook, ValidateAndTransformComposite, LifeCycle, ParallelCompositeHook
from hooks.triggers import EmitEventHook
from hooks.core.setters import IdAssignerHook, PasswordHasherHook, ComputedFieldsHook, StaticFieldSetterHook
from hooks.core.validators import RequiredFieldsHook, RelationExistsHook
from hooks.functions import assign_id, set_timestamp, hash_password, send_welcome_email
from example.user.repositories.country_repository import CountryRelationRepository
# from example.user.service.methods.country_setter import RelatedCountryAssignerHook

before_validations = [
    RequiredFieldsHook(["username", "password", "country_id"]),
    RelationExistsHook(CountryRelationRepository(), "country_id") # Relation validation
]

before_transformations = [
    PasswordHasherHook(hash_password),
    StaticFieldSetterHook(verified=False, role="standard", active=True),
    IdAssignerHook(assign_id),
    ComputedFieldsHook(set_timestamp)
    # RelatedCountryAssignerHook(CountryRelationRepository(), "country_id") # Not implemented yet.
]

after_triggers = [
    EmitEventHook("UserCreated", lambda data: print(f"[Event:UserCreated] User created successfully. (ID {data.id})")),
    EmitEventHook("UserCreated", send_welcome_email),
    EmitEventHook("UserCreated", send_welcome_email)
]

create_life_cycle = LifeCycle(
    before=ValidateAndTransformComposite(
        validations=ParallelCompositeHook(before_validations),
        transformations=AsyncCompositeHook(before_transformations)
    ),
    after=ParallelCompositeHook(after_triggers)
)
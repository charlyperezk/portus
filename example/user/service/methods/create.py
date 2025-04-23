from hooks.base import CompositeHook, ValidateAndTransformComposite, LifeCycle
from hooks.triggers import EmitEventHook
from hooks.core.setters import IdAssignerHook, PasswordHasherHook, ComputedFieldsHook, StaticFieldSetterHook
from hooks.core.validators import RequiredFieldsHook
from hooks.functions import assign_id, set_timestamp, hash_password, send_welcome_email

before_transformations = [
    PasswordHasherHook(hash_password),
    StaticFieldSetterHook(verified=False, role="standard", active=True),
    IdAssignerHook(assign_id),
    ComputedFieldsHook(set_timestamp)
]

before_validations = [
    RequiredFieldsHook(["username", "password"]),
    # RequiredFieldsHook(["username", "password", "province_id"]),
    # RelationExistsHook("ProvinceRepo", "province_id")
]

after_triggers = [
    EmitEventHook("UserCreated", lambda data: print(f"[Event:UserCreated] User created successfully. (ID {data.id})")),
    EmitEventHook("UserCreated", send_welcome_email)
]

create_life_cycle = LifeCycle(
    before=ValidateAndTransformComposite(
        validations=CompositeHook(before_validations),
        transformations=CompositeHook(before_transformations)
    ),
    after=CompositeHook(after_triggers)
)
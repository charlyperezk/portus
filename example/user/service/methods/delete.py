from hooks.base import CompositeHook, ValidateAndTransformComposite, LifeCycle, ParallelCompositeHook
from hooks.triggers import EmitEventHook
from hooks.core.setters import ComputedFieldsHook, StaticFieldSetterHook
from hooks.functions import set_update_time

before_transformations = [
    ComputedFieldsHook(set_update_time),
    StaticFieldSetterHook(active=False)
]

before_validations = [
]

after_triggers = [
    EmitEventHook("UserDeleted", lambda data: print(f"[Event:UserDeleted] User deleted successfully. (ID {data.id})"))
]

delete_life_cycle = LifeCycle(
    before=ValidateAndTransformComposite(
        validations=ParallelCompositeHook(before_validations),
        transformations=CompositeHook(before_transformations)
    ),
    after=ParallelCompositeHook(after_triggers)
)
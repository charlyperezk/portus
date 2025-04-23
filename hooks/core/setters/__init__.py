from hooks.core.setters.utils import ComputedFieldsHook, IdAssignerHook, PasswordHasherHook
from hooks.core.setters.static_setter import StaticFieldSetterHook
from hooks.core.setters.related_field import RelationFieldAssignerHook

__all__ = [
    "ComputedFieldsHook"
    "StaticFieldSetterHook",
    "IdAssignerHook",
    "PasswordHasherHook",
    "RelationFieldAssignerHook"
]
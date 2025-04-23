from core.types import TInternalData
from hooks.core.setters.compute_fields import ComputedFieldsHook

class IdAssignerHook(ComputedFieldsHook):
    def __call__(self, data: TInternalData) -> TInternalData:
        return data.assign_id(self._compute_fn)
    
class PasswordHasherHook(ComputedFieldsHook):
    def __call__(self, data: TInternalData) -> TInternalData:
        return data.assign_hashed_password(self._compute_fn)
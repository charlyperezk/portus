from typing import Any
from core.types import TInternalData
from hooks.base.hook import Hook

class StaticFieldSetterHook(Hook):
    def __init__(self, **static_fields: Any):
        self._static_fields = static_fields

    def __call__(self, data: TInternalData) -> TInternalData:
        return data.merge(self._static_fields)
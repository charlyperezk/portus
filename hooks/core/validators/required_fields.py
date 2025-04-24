from typing import List, Optional
from common.types import TInternalData
from hooks.base.hook import Hook

class RequiredFieldsHook(Hook):
    def __init__(self, fields: List[str]):
        self.fields = fields

    def __call__(self, data: TInternalData) -> Optional[TInternalData]:
        missing = [f for f in self.fields if not data.contains(f)]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
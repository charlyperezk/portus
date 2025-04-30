from typing import Union, Dict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class ContextFlag:
    @staticmethod
    def is_flag() -> bool:
        return True

@dataclass(frozen=True)
class RelatedFieldContext(ContextFlag):
    key: str
    value: Union[str, Dict[str, Any]]
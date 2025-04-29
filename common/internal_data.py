from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass(frozen=True)
class InternalData:
    data: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name: str) -> Any:
        value = self.data.get(name)
        if value == None:
            raise AttributeError(f"{name} not found in InternalData")
        return value

    def get_value(self, name: str) -> Any:
        return self.__getattr__(name)

    def with_value(self, key: str, value: Any) -> "InternalData":
        return InternalData({**self.data, key: value}, context=self.context)

    def merge(self, other: Dict[str, Any]) -> "InternalData":
        return InternalData({**self.data, **other}, context=self.context)

    def to_dict(self) -> Dict[str, Any]:
        context_keys = [key for key in self.data.keys() if not key.startswith("__")]
        data = {k: self.__getattr__(k) for k in context_keys}
        return data

    def contains(self, key: str) -> bool:
        return key in self.data

    def validate_required(self, fields: list[str]) -> "InternalData":
        missing = [f for f in fields if f not in self.data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        return self
    
    def get_context(self) -> Dict[str, Any]:
        return self.context
    
    def set_context(self, key: str, value: Any) -> "InternalData":
        return InternalData(self.data, {**self.context, key: value})

    def without_value(self, key: str) -> "InternalData":
        data = {k: v for k, v in self.data.items() if k != key}
        return InternalData(data)
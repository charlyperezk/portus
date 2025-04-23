from dataclasses import dataclass
from typing import Callable, Any, Dict, TypeVar

T_ID = TypeVar("T_ID")

@dataclass(frozen=True)
class InternalData:
    data: Dict[str, Any]

    def __getattr__(self, name: str) -> Any:
        try:
            return self.data[name]
        except KeyError:
            raise AttributeError(f"{name} not found in InternalData")

    def with_value(self, key: str, value: Any) -> "InternalData":
        return InternalData({**self.data, key: value})

    def merge(self, other: Dict[str, Any]) -> "InternalData":
        return InternalData({**self.data, **other})

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)

    def contains(self, key: str) -> bool:
        return key in self.data

    def assign_id(self, f: Callable[[], T_ID]) -> "InternalData":
        return self.with_value("id", f())
    
    def assign_hashed_password(self, f: Callable[[], T_ID]) -> "InternalData":
        data = self.to_dict()
        password_hash = f(self.__getattr__('password'))
        del data['password']
        return InternalData(data).with_value("password_hash", password_hash)

    def validate_required(self, fields: list[str]) -> "InternalData":
        missing = [f for f in fields if f not in self.data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        return self


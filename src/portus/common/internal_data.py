from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union, List, Callable
from portus.common.context_schemas import ContextFlag, RelatedFieldContext

@dataclass(frozen=True)
class InternalData:
    data: Dict[str, Any]
    context: Dict[str, Union[ContextFlag, RelatedFieldContext, Any]] = field(default_factory=dict)
    trace: List[str] = field(default_factory=list)

    def __getattr__(self, name: str) -> Any:
        value = self.data.get(name)
        if value == None:
            raise AttributeError(f"{name} not found in InternalData")
        return value

    def get_value(self, name: str) -> Any:
        return self.__getattr__(name)

    def with_value(self, key: str, value: Any) -> "InternalData":
        traced_value = value if not key.endswith("_hash") else "**hide**"
        new_trace = self.trace + [f"Set value: {key} = {traced_value}"]
        return InternalData({**self.data, key: value}, context=self.context, trace=new_trace)

    def merge(self, other: Dict[str, Any]) -> "InternalData":
        new_trace = self.trace + [f"Merged with: {other}"]
        return InternalData({**self.data, **other}, context=self.context, trace=new_trace)

    def to_dict(self) -> Dict[str, Any]:
        return self.data

    def contains(self, key: str) -> bool:
        return key in self.data

    def validate_required(self, fields: list[str]) -> "InternalData":
        missing = [f for f in fields if f not in self.data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        return self
    
    def without_value(self, key: str) -> "InternalData":
        new_trace = self.trace + [f"Remove key: {key}"]
        data = {k: v for k, v in self.data.items() if k != key}
        return InternalData(data=data, context=self.context, trace=new_trace)

    def get_context(self) -> Dict[str, Any]:
        return self.context
    
    def with_context(self, key: str, value: Any) -> "InternalData":
        new_trace = self.trace + [f"Set context: {key} = {value}"]
        return InternalData(self.data, {**self.context, key: value}, trace=new_trace)

    def get_value_from_context(self, key: str) -> Optional[Any]:
        return self.context.get(key, None)
    
    def set_context_flag(self, key: str, flag: Optional[ContextFlag]=ContextFlag) -> "InternalData":
        return self.with_context(key, flag)

    def get_flags_within_context(self, prefix: Optional[str] = None) -> Dict[str, ContextFlag]:
        flags = {
            k: v
            for k, v in self.context.items()
            if hasattr(v, "is_flag") and v.is_flag()
        }
        if prefix:
            return {k: v for k, v in flags.items() if k.startswith(prefix)}
        return flags
        
    def print_trace(
        self,
        prefix: str = "Trace",
        with_index: bool = True,
        logger: Optional[Callable[[str], None]] = print
    ) -> None:
        message = f"{prefix} summary ({len(self.trace)} steps):"
        for i, entry in enumerate(self.trace):
            index = f"[{i+1}] " if with_index else "- "
            message += f"\n\t{index}{entry}"
        
        logger(message)

from typing import Callable, Any, Dict, Awaitable, Optional
from common.types import TInternalData
from hooks.transformer import DataTransformerHook

def make_static_field_hook(field: str, value_fn: Callable[[], Any]) -> DataTransformerHook:
    def with_value(data: TInternalData):
        return data.with_value(field, value_fn())
    
    return DataTransformerHook(with_value)

def make_static_fields_hook(fields: Dict[str, Any]) -> DataTransformerHook:
    def merge(data: TInternalData):
        return data.merge(fields)
    
    return DataTransformerHook(merge)

def make_computed_fields_hook(compute_fn: Callable[[TInternalData], Dict[str, Any]]) -> DataTransformerHook:
    async def transform(data: TInternalData) -> TInternalData:
        computed = compute_fn(data)
        if isinstance(computed, Awaitable):
            computed = await computed
        return data.merge(computed)
    return DataTransformerHook(transform)

def make_hash_field_hook(
    field: str,
    hash_function: Callable[[str], str],
    key_name: Optional[str] = None,
    exclude_unhashed: bool = True,
) -> DataTransformerHook:
    async def transform(data: TInternalData) -> TInternalData:
        value_to_hash = data.get_value(field)
        hashed_value = hash_function(value_to_hash)
        key = key_name or f"{field}_hash"
        data = data.with_value(key, hashed_value)
        if exclude_unhashed:
            data = data.without_value(field)
        return data
    return DataTransformerHook(transform)
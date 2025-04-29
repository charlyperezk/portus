from dataclasses import asdict
from typing import Callable, Optional
from common.types import TInternalData
from ports.output.repository import GetAndAskRepository
from hooks.transformer import DataTransformerHook

def make_relation_context_hook(
    field: str,
    repository: GetAndAskRepository,
    key_name: Optional[str] = None,
    transform_entity: Callable = lambda e: asdict(e),
) -> DataTransformerHook:
    async def transform(data: TInternalData) -> TInternalData:
        id_value = data.get_value(field)
        entity = repository.get(id_value)
        key = key_name or field.replace("_id", "")
        return data.set_context(key, transform_entity(entity))
    return DataTransformerHook(transform)
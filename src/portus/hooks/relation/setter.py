from dataclasses import asdict
from typing import Callable, Optional, Dict, Union, Any
from portus.common.types import TInternalData, TEntity, T_ID, RELATION_SETTED_FLAG, RelatedFieldContext
from portus.ports.output.repository import GetAndAskRepository
from portus.hooks.transformer import DataTransformerHook

def relation_context_hook(
    field: str,
    repository: GetAndAskRepository[T_ID, TEntity],
    key_name: Optional[str] = None,
    transform_entity: Callable[[TEntity], Union[Dict[str, Any], Any]] = lambda e: asdict(e),
) -> DataTransformerHook:
    async def transform(data: TInternalData) -> TInternalData:
        id_value = data.get_value(field)
        entity = await repository.get(id_value)
        key = key_name or field.replace("_id", "")
        flag_identifier = f"{RELATION_SETTED_FLAG}_{key}"
        return data.set_context_flag(
            key=flag_identifier,
            flag=RelatedFieldContext(
                key=key,
                value=transform_entity(entity)
            )
        )
    return DataTransformerHook(transform)
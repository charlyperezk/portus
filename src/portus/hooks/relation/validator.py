from portus.hooks.validator import DataValidatorHook
from portus.common.types import TInternalData
from portus.ports.output.repository import GetAndAskRepository

def relation_exists_hook(
    field: str,
    repository: GetAndAskRepository
    ) -> DataValidatorHook:
    async def validate(data: TInternalData):
        id = data.get_value(field)
        exists = await repository.exists(id)
        if not exists:
            raise ValueError(f"Related entity with id {id} not found")
        return data
    return DataValidatorHook(validate)

def is_inactive_hook(field: str) -> DataValidatorHook:
    async def validate(data: TInternalData):
        active = data.get_value(field)
        if not active:
            raise ValueError(f"Related entity with id {data.get_value("id")} not found")
        return data
    return DataValidatorHook(validate)

from hooks.validator import DataValidatorHook
from common.types import TInternalData
from ports.output.repository import GetAndAskRepository

def make_relation_exists_hook(
    field: str,
    repository: GetAndAskRepository
    ) -> DataValidatorHook:
    async def validate(data: TInternalData):
        id = data.get_value(field)
        exists = repository.exists(id)
        if not exists:
            raise ValueError(f"Related entity with id {id} not found")
    return DataValidatorHook(validate)
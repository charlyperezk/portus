from hooks.validator import DataValidatorHook
from common.types import TInternalData
from ports.output.repository import GetByEmailPort

def require_fields(fields: list[str]) -> DataValidatorHook:
    def validate(data: TInternalData):
        missing = [f for f in fields if not data.contains(f)]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
    return DataValidatorHook(validate)

def make_check_unique_email_hook(
    field: str,
    repository: GetByEmailPort
    ) -> DataValidatorHook:
    async def validate(data: TInternalData):
        email = data.get_value(field)
        exists = await repository.find_by_email(email)
        if exists:
            raise ValueError(f"Email {email} is already registered")
        return data
    return DataValidatorHook(validate)
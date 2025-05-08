from portus.ports.output.repository import GetByEmailPort
from portus.common.types import TInternalData
from portus.common.exceptions import ValidationError
from portus.hooks.validator import DataValidatorHook

def require_fields(fields: list[str]) -> DataValidatorHook:
    def validate(data: TInternalData):
        missing = [f for f in fields if not data.contains(f)]
        if missing:
            raise ValidationError(f"Missing required fields: {missing}")
        return data
    return DataValidatorHook(validate)

def check_unique_email_hook(
    field: str,
    repository: GetByEmailPort
    ) -> DataValidatorHook:
    async def validate(data: TInternalData):
        email = data.get_value(field)
        exists = await repository.find_by_email(email)
        if exists:
            raise ValidationError(f"Email {email} is already registered")
        return data
    return DataValidatorHook(validate)
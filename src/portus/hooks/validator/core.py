from typing import Callable, Awaitable, Union
from portus.hooks.base import BaseHook
from portus.common.types import TInternalData
from portus.common.exceptions import ValidationError

ValidationFn = Callable[[TInternalData], Union[None, Awaitable[None]]]

class DataValidatorHook(BaseHook):
    def __init__(self, validation_fn: ValidationFn):
        self.validation_fn = validation_fn

    async def __call__(self, data: TInternalData) -> TInternalData:
        try:
            result = self.validation_fn(data)
            return await self._maybe_await(result)
        except Exception as e:
            raise ValidationError(e)
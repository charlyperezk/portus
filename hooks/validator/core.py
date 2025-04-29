from hooks.base import BaseHook
from common.types import TInternalData
from typing import Callable, Awaitable, Union

ValidationFn = Callable[[TInternalData], Union[None, Awaitable[None]]]

class DataValidatorHook(BaseHook):
    def __init__(self, validation_fn: ValidationFn):
        self.validation_fn = validation_fn

    async def __call__(self, data: TInternalData) -> TInternalData:
        result = self.validation_fn(data)
        return await self._maybe_await(result)
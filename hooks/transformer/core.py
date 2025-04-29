from hooks.base import BaseHook
from common.types import TInternalData
from typing import Callable, Awaitable, Union

TransformFn = Callable[[TInternalData], Union[TInternalData, Awaitable[TInternalData]]]

class DataTransformerHook(BaseHook):
    def __init__(self, transform_fn: TransformFn):
        self.transform_fn = transform_fn

    async def __call__(self, data: TInternalData) -> TInternalData:
        result = self.transform_fn(data)
        return await self._maybe_await(result)
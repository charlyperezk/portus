from hooks.base import BaseHook
from common.types import TInternalData
from typing import Callable, Awaitable, Union

TriggererFn = Callable[[TInternalData], Union[None, Awaitable[None]]]

class DataTriggererHook(BaseHook):
    def __init__(self, triggerer_fn: TriggererFn):
        self.triggerer_fn = triggerer_fn

    async def __call__(self, data: TInternalData) -> Union[None, Awaitable[None]]:
        result = self.triggerer_fn(data)
        return await self._maybe_await(result)
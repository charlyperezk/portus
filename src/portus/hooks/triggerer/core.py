from typing import Callable, Awaitable, Union
from portus.hooks.base import BaseHook
from portus.common.types import TInternalData
from portus.common.exceptions import TriggerError

TriggererFn = Callable[[TInternalData], Union[None, Awaitable[None]]]

class DataTriggererHook(BaseHook):
    def __init__(self, triggerer_fn: TriggererFn):
        self.triggerer_fn = triggerer_fn

    async def __call__(self, data: TInternalData) -> Union[None, Awaitable[None]]:
        try:
            result = self.triggerer_fn(data)
            return await self._maybe_await(result)
        except Exception as e:
            raise TriggerError(e)
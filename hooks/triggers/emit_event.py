from typing import Callable, Any
from common.types import TInternalData
from hooks.base.hook import AsyncHook

class EmitEventHook(AsyncHook):
    def __init__(self, event_name: str, callback: Callable[[TInternalData], Any]):
        self.event_name = event_name
        self.callback = callback

    async def __call__(self, data: TInternalData) -> TInternalData:
        print(f"[Event:{self.event_name}] Executing callback ({self.callback.__name__.upper()})")
        result = self.callback(data)
        if hasattr(result, "__await__"):
            await result
        return data
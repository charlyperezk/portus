from abc import ABC, abstractmethod
from typing import Generic, List, Union
from core.types import TInternalData

class Hook(ABC, Generic[TInternalData]):
    @abstractmethod
    def __call__(self, data: TInternalData) -> TInternalData: ...    

class AsyncHook(ABC, Generic[TInternalData]):
    @abstractmethod
    async def __call__(self, data: TInternalData) -> TInternalData: ...

class CompositeHook:
    def __init__(self, hooks: List[Union[Hook, AsyncHook]]):
        self.hooks = hooks

    async def run(self, data: TInternalData) -> TInternalData:
        for hook in self.hooks:
            result = hook(data)
            data = await result if hasattr(result, "__await__") else result
        return data

    async def __call__(self, data: TInternalData) -> TInternalData:
        return await self.run(data)

    @classmethod
    def from_hooks(cls, hooks: List[Union[Hook, AsyncHook]]) -> 'CompositeHook':
        return cls(hooks)
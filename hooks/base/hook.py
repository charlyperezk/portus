from abc import ABC, abstractmethod
from typing import Generic, List, Union
from common.types import TInternalData
import asyncio

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

class ParallelCompositeHook(CompositeHook):
    """
    Runs all hooks in parallel as tasks without waiting for their results.
    Ideal for side-effects (logging, events, metrics).
    Immediately returns the same input `data`.
    """
    async def run(self, data: TInternalData) -> TInternalData:
        tasks = []
        for hook in self.hooks:
            result = hook(data)
            if hasattr(result, "__await__"):
                tasks.append(asyncio.create_task(result))
            else:
                tasks.append(asyncio.create_task(asyncio.to_thread(hook, data)))
        _ = asyncio.gather(*tasks, return_exceptions=True)
        return data

    async def __call__(self, data: TInternalData) -> TInternalData:
        return await self.run(data)

    @classmethod
    def from_hooks(cls, hooks: List[Union[Hook, AsyncHook]]) -> 'ParallelCompositeHook':
        return cls(hooks)
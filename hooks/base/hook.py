from abc import ABC, abstractmethod
from typing import Generic, List, Union, Optional
from common.types import TInternalData
import asyncio

class Hook(ABC, Generic[TInternalData]):
    @abstractmethod
    def __call__(self, data: TInternalData) -> TInternalData: ...    

class AsyncHook(ABC, Generic[TInternalData]):
    @abstractmethod
    async def __call__(self, data: TInternalData) -> TInternalData: ...

class HookContainer(ABC, Generic[TInternalData]):
    def __init__(self, hooks: List[Union[Hook, AsyncHook]]):
        self.hooks = hooks

    @abstractmethod
    def run(self, data: TInternalData) -> Optional[TInternalData]:
        pass

    @abstractmethod
    def __call__(self, data: TInternalData) -> Optional[TInternalData]:
        pass

class AsyncCompositeHook(HookContainer[TInternalData]):
    async def run(self, data: TInternalData) -> TInternalData:
        for hook in self.hooks:
            result = hook(data)
            data = await result if hasattr(result, "__await__") else result
        return data

    async def __call__(self, data: TInternalData) -> TInternalData:
        return await self.run(data)

class ParallelCompositeHook(HookContainer):
    """
    Runs all hooks in parallel as tasks without waiting for their results.
    Ideal for side-effects (logging, events, metrics).
    Immediately returns the same input `data`.
    """
    def __init__(self, hooks: List[Union[Hook, AsyncHook]]):
        self.hooks = hooks

    async def run(self, data: TInternalData) -> TInternalData:
        tasks = []
        for hook in self.hooks:
            result = hook(data)
            if hasattr(result, "__await__"):
                # es coroutine, lanzamos como tarea
                tasks.append(asyncio.create_task(result))
            else:
                # es síncrono, ejecutarlo en el loop inmediatamente
                # y envolverlo en tarea para mantener consistencia
                tasks.append(asyncio.create_task(asyncio.to_thread(hook, data)))
        # lanzamos todas en paralelo, pero no esperamos a que terminen
        # Si quisieras capturar excepciones, podrías hacer:
        # asyncio.gather(*tasks, return_exceptions=True)
        # Pero aquí las ignoramos para no bloquear
        _ = await asyncio.gather(*tasks, return_exceptions=True)
        return data

    async def __call__(self, data: TInternalData) -> TInternalData:
        return await self.run(data)
import inspect
from abc import ABC, abstractmethod
from typing import Optional
from common.types import TInternalData

class BaseHook(ABC):
    @abstractmethod
    def __call__(self, data: TInternalData) -> Optional[TInternalData]:
        ...
    
    async def _maybe_await(self, result):
        if inspect.isawaitable(result):
            return await result
        return result
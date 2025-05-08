from abc import ABC, abstractmethod
from typing import Optional
from portus.common.types import TInternalData
from portus.utils.functions import maybe_await

class BaseHook(ABC):
    @abstractmethod
    def __call__(self, data: TInternalData) -> Optional[TInternalData]:
        ...
    
    async def _maybe_await(self, result: TInternalData) -> TInternalData:
        return await maybe_await(result)
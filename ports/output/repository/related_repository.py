from abc import ABC, abstractmethod
from core.types import TEntity, T_ID
from ports.output.repository import GetPort

class RelationRepository(GetPort[TEntity, T_ID], ABC):
    @abstractmethod
    def exists(self, id: T_ID) -> bool: ...
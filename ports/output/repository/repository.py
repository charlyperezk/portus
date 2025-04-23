from abc import ABC, abstractmethod
from typing import Generic
from common.types import T_ID, TEntity
 
class SavePort(Generic[TEntity], ABC):
    @abstractmethod
    def save(self, object: TEntity) -> TEntity: ...

class GetPort(Generic[TEntity, T_ID], ABC):
    @abstractmethod
    def get(self, id: T_ID) -> TEntity: ...

class ListPort(Generic[TEntity], ABC):
    @abstractmethod
    def list_all(self) -> list[TEntity]: ...

class DeletePort(Generic[T_ID], ABC):
    @abstractmethod
    def delete(self, id: T_ID) -> None: ...

class CrudRepository(SavePort[TEntity], GetPort[TEntity, T_ID], ListPort[TEntity], DeletePort[T_ID], ABC):
    @abstractmethod
    def assign_id(self) -> T_ID: ...
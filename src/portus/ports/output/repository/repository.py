from abc import ABC, abstractmethod
from typing import Generic, Optional
from portus.common.types import T_ID, TEntity
 
class SavePort(Generic[TEntity], ABC):
    @abstractmethod
    def save(self, object: TEntity) -> TEntity: ...

class GetPort(Generic[T_ID, TEntity], ABC):
    @abstractmethod
    def get(self, id: T_ID) -> TEntity: ...

class UpdatePort(Generic[TEntity], ABC):
    @abstractmethod
    def update(self, entity: TEntity) -> TEntity: ...

class ListPort(Generic[TEntity], ABC):
    @abstractmethod
    def list_all(self) -> list[TEntity]: ...

class DeletePort(Generic[T_ID], ABC):
    @abstractmethod
    def delete(self, id: T_ID) -> bool: ...

class CrudRepository(
    Generic[TEntity, T_ID],
    GetPort[T_ID, TEntity],
    UpdatePort[TEntity],
    SavePort[TEntity],
    ListPort[TEntity],
    DeletePort[T_ID], ABC
):
    @abstractmethod
    def assign_id(self) -> T_ID: ...

class ExistsPort(Generic[T_ID], ABC):
    @abstractmethod
    def exists(self, id: T_ID) -> bool: ...
    
class GetAndAskRepository(GetPort[T_ID, TEntity], ExistsPort[T_ID], ABC):
    ...

class GetByEmailPort(Generic[TEntity], ABC):
    def find_by_email(self, email: str) -> Optional[TEntity]:
        ...
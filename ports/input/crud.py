from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T_ID = TypeVar('T_ID')
T_CreateDTO = TypeVar('T_CreatePosDTO')
T_ReadDTO = TypeVar('T_ReadDTO')
T_UpdateDTO = TypeVar('T_UpdateDTO')
T_DeleteDTO = TypeVar('T_DeleteDTO')

class CreatePort(ABC, Generic[T_CreateDTO, T_ReadDTO, T_ID]):
    @abstractmethod
    def create(self, dto: T_CreateDTO) -> T_ReadDTO: ...

class ListAllPort(ABC, Generic[T_ReadDTO, T_ID]):
    @abstractmethod
    def get(self, id: T_ID) -> T_ReadDTO: ...

    @abstractmethod
    def list_all(self) -> list[T_ReadDTO]: ...

class UpdatePort(ABC, Generic[T_UpdateDTO, T_ID]):
    @abstractmethod
    def update(self, id: T_ID, dto: T_UpdateDTO) -> None: ...

class DeletePort(ABC, Generic[T_ID]):
    @abstractmethod
    def delete(self, id: T_ID) -> None: ...

class CRUDPort(
    CreatePort[T_CreateDTO, T_ReadDTO, T_ID],
    ListAllPort[T_ReadDTO, T_ID],
    UpdatePort[T_UpdateDTO, T_ID],
    DeletePort[T_ID],
    ABC
): 
    """
    Port that combines all CRUD operations.
    """
    pass
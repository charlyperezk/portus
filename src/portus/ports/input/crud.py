from abc import ABC, abstractmethod
from typing import Generic
from portus.common.types import T_ID, TCreateDTO, TReadDTO, TUpdateDTO, TInternalData

class CreatePort(ABC, Generic[TCreateDTO, TReadDTO, T_ID]):
    @abstractmethod
    def create(self, dto: TCreateDTO) -> TReadDTO: ...

class GetPort(ABC, Generic[TReadDTO, T_ID]):
    @abstractmethod
    def get(self, id: T_ID) -> TReadDTO: ...

class ListAllPort(ABC):
    @abstractmethod
    def list_all(self) -> list[TReadDTO]: ...

class UpdatePort(ABC, Generic[TUpdateDTO, T_ID]):
    @abstractmethod
    def update(self, id: T_ID, dto: TUpdateDTO) -> None: ...

class DeletePort(ABC, Generic[T_ID]):
    @abstractmethod
    def delete(self, id: T_ID) -> None: ...

class CRUDPort(
    Generic[T_ID, TCreateDTO, TReadDTO, TUpdateDTO],
    CreatePort[T_ID, TCreateDTO, TReadDTO], ListAllPort, GetPort[T_ID, TReadDTO],
    UpdatePort[T_ID, TUpdateDTO], DeletePort[T_ID], ABC): 
    ...
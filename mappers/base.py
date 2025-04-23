from abc import ABC, abstractmethod
from typing import Generic, Any
from core.types import TEntity, TReadDTO, TInternalData, TCreateDTO

class Mapper(ABC, Generic[TEntity, TReadDTO, TCreateDTO, TInternalData]):
    @abstractmethod
    def to_dict(self, entity: TEntity) -> dict[str, Any]: ...

    @abstractmethod
    def to_dto(self, entity: TEntity) -> TReadDTO: ...
    
    @abstractmethod
    def to_internal_data(self, dto: TCreateDTO, **kwargs) -> TInternalData: ...

    @abstractmethod
    def from_internal_data(self, data: TInternalData) -> TReadDTO: ...

    @abstractmethod
    def merge_changes(self, entity: TEntity, data: TInternalData) -> TEntity: ...

    @abstractmethod
    def from_entity_to_internal_data(self, entity: TEntity) -> TInternalData: ...
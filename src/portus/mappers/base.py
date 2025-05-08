from abc import ABC, abstractmethod
from dataclasses import is_dataclass
from typing import Generic, Type, Any, Optional, Dict
from portus.common.types import TEntity, TCreateDTO, TReadDTO, TInternalData

class Mapper(ABC, Generic[TEntity, TCreateDTO, TReadDTO, TInternalData]):
    def __init__(
        self,
        entity_cls: Type[TEntity],
        read_dto_cls: Type[TReadDTO],
        internal_data_cls: Type[TInternalData],
    ):
        assert is_dataclass(entity_cls), "Entity must be a dataclass"
        self.entity_cls = entity_cls
        self.read_dto_cls = read_dto_cls
        self.internal_data_cls = internal_data_cls

    @abstractmethod
    def to_dict(self, entity: TEntity) -> dict[str, Any]: ...

    @abstractmethod
    def to_dto(self, entity: TEntity, context: Optional[Dict[str, Any]]) -> TReadDTO: ...

    @abstractmethod
    def to_entity(self, dto: TCreateDTO) -> TEntity: ...

    @abstractmethod
    def to_internal_data(self, dto: TCreateDTO, **kwargs) -> TInternalData: ...

    @abstractmethod
    def from_internal_data(self, data: TInternalData) -> TEntity: ...

    @abstractmethod
    def merge_changes(self, entity: TEntity, data: TInternalData) -> TEntity: ...

    @abstractmethod
    def from_entity_to_internal_data(self, entity: TEntity) -> TInternalData: ...

    @abstractmethod
    def define_unset_fields_from_entity(self, entity: TEntity, dto: TCreateDTO) -> TInternalData: ...
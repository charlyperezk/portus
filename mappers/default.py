from dataclasses import asdict, fields, is_dataclass
from typing import Type, Generic

from pydantic import BaseModel
from common.types import TEntity, TReadDTO, TInternalData
from mappers.base import Mapper

class DefaultMapper(Generic[TEntity, TReadDTO, TInternalData], Mapper[TEntity, TReadDTO, BaseModel, TInternalData]):
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

    def to_internal_data(self, dto: BaseModel) -> TInternalData:
        data = dto.model_dump(exclude_unset=True)
        return self.internal_data_cls(data)

    def from_internal_data(self, data: TInternalData) -> TEntity:
        field_names = {f.name for f in fields(self.entity_cls)}
        missed_values = [field_name 
                         for field_name in field_names if not data.contains(field_name)]
        if any(missed_values):
            raise Exception(f"You are missing {len(missed_values)} fields: {missed_values}")
        expected_data = {field_name: data.__getattr__(field_name) for field_name in field_names}
        return self.entity_cls(**expected_data)

    def to_dto(self, entity: TEntity) -> TReadDTO:
        return self.read_dto_cls(**asdict(entity))

    def to_dict(self, entity: TEntity) -> dict:
        return asdict(entity)
    
    def from_entity_to_internal_data(self, entity: TEntity) -> TInternalData:
        return self.internal_data_cls(self.to_dict(entity))

    def merge_changes(self, entity: TEntity, data: TInternalData) -> TEntity:
        entity_as_internal_data = self.internal_data_cls(self.to_dict(entity))
        merged_data = entity_as_internal_data.merge(other=data.to_dict())
        return self.from_internal_data(merged_data)
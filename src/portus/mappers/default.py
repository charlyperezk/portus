from dataclasses import asdict, fields
from pydantic import BaseModel
from typing import Dict, Optional
from portus.mappers.base import Mapper
from portus.common.types import (
    TEntity,
    TCreateDTO,
    TReadDTO,
    TUpdateDTO,
    TInternalData,
    RelatedFieldContext,
)

class DefaultMapper(Mapper[TEntity, TCreateDTO, TReadDTO, TInternalData]):
    def to_internal_data(self, dto: BaseModel) -> TInternalData:
        data = dto.model_dump(exclude_unset=True)
        return self.internal_data_cls(data)

    def from_internal_data(self, data: TInternalData) -> TEntity:
        field_names = {f.name for f in fields(self.entity_cls)}
        missed_values = [field_name 
                         for field_name in field_names if not data.contains(field_name)]
        if any(missed_values):
            raise Exception(f"You are missing {len(missed_values)} fields: {missed_values}")
        expected_data = {field_name: data.get_value(field_name) for field_name in field_names}
        return self.entity_cls(**expected_data)

    def to_dto(self, entity: TEntity,
                context_flags: Optional[Dict[str, RelatedFieldContext]]=None) -> TReadDTO:
        data = asdict(entity)

        if context_flags:
            context_relation_data = {
                v.key: v.value for _, v in context_flags.items()
            }
            data.update(**context_relation_data)
        
        return self.read_dto_cls(**data)

    def to_dict(self, entity: TEntity) -> dict:
        return asdict(entity)

    def to_entity(self, dto: TCreateDTO) -> TEntity:
        data = dto.model_dump(exclude_unset=True)
        return self.entity_cls(**data)

    def from_entity_to_internal_data(self, entity: TEntity) -> TInternalData:
        return self.internal_data_cls(self.to_dict(entity))

    def merge_changes(self, entity: TEntity, data: TInternalData) -> TEntity:
        entity_as_internal_data = self.internal_data_cls(self.to_dict(entity))
        merged_data = entity_as_internal_data.merge(other=data.to_dict())
        return self.from_internal_data(merged_data)
    
    def define_unset_fields_from_entity(self, entity: TEntity, dto: TUpdateDTO) -> TInternalData:
        internal_data = self.internal_data_cls(self.to_dict(entity))
        dto_dict = dto.model_dump(exclude_unset=True)
        return internal_data.merge(dto_dict)
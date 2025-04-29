from dataclasses import asdict, fields
from pydantic import BaseModel
from typing import Dict, Any
from mappers.base import Mapper
from common.types import TEntity, TCreateDTO, TReadDTO, TInternalData

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

    def to_dto(self, entity: TEntity, context: Dict[str, Any]) -> TReadDTO:
        data = asdict(entity)
        if context:
            data.update(**context)
        return self.read_dto_cls(**data)

    def to_dict(self, entity: TEntity) -> dict:
        return asdict(entity)
    
    def from_entity_to_internal_data(self, entity: TEntity) -> TInternalData:
        return self.internal_data_cls(self.to_dict(entity))

    def merge_changes(self, entity: TEntity, data: TInternalData) -> TEntity:
        entity_as_internal_data = self.internal_data_cls(self.to_dict(entity))
        merged_data = entity_as_internal_data.merge(other=data.to_dict())
        return self.from_internal_data(merged_data)
    
    def define_unset_fields_from_entity(self, entity: TEntity, dto: TCreateDTO) -> TInternalData:
        dto_dict = dto.model_dump()
        dict_of_unsetted = {k: v for k, v in dto_dict.items() if not v}
        data_obtained_from_entity = {k: v for k, v in asdict(entity).items() if k in dict_of_unsetted}
        return self.internal_data_cls(dto_dict).merge(data_obtained_from_entity)
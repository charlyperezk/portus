from dataclasses import asdict, fields
from pydantic import BaseModel
from mappers.base import Mapper
from common import InternalData, TEntity, TReadDTO

class DefaultMapper(Mapper[TEntity, TReadDTO, BaseModel, InternalData]):
    def to_internal_data(self, dto: BaseModel) -> InternalData:
        data = dto.model_dump(exclude_unset=True)
        return self.internal_data_cls(data)

    def from_internal_data(self, data: InternalData) -> TEntity:
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
    
    def from_entity_to_internal_data(self, entity: TEntity) -> InternalData:
        return self.internal_data_cls(self.to_dict(entity))

    def merge_changes(self, entity: TEntity, data: InternalData) -> TEntity:
        entity_as_internal_data = self.internal_data_cls(self.to_dict(entity))
        merged_data = entity_as_internal_data.merge(other=data.to_dict())
        return self.from_internal_data(merged_data)
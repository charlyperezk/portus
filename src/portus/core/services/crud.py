from typing import List, Generic
from portus.ports.input.crud import CRUDPort
from portus.core.services.default import DefaultService
from portus.common.exceptions import ValidationError
from portus.common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TUpdateDTO,
    TReadDTO,
    TInternalData,
)

class CRUDService(
    DefaultService[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData],
    CRUDPort[TCreateDTO, TReadDTO, TUpdateDTO, T_ID],
    Generic[TEntity, T_ID, TCreateDTO, TReadDTO, TInternalData, TUpdateDTO]
):
    async def create(self, dto: TCreateDTO) -> TReadDTO:        
        entity = self.mapper.to_entity(dto)
        result = await self._persist(entity)
        entity_name = entity.__class__.__name__
        self.logger.info(f"{entity_name} created with ID {result.id}")
        return self.mapper.to_dto(result)
    
    async def update(self, id: T_ID, dto: TUpdateDTO) -> TReadDTO:
        entity = await self.repository.get(id)
        if not entity:
            raise ValidationError.id_not_exists(id)
        self.logger.debug(f"Detected changes {dto.model_dump(exclude_unset=True)}")
        data = self.mapper.define_unset_fields_from_entity(entity, dto)
        entity = self.mapper.merge_changes(entity, data)
        await self.repository.update(entity)        
        entity_name = entity.__class__.__name__
        self.logger.info(f"{entity_name} updated with ID {entity.id}")        
        return self.mapper.to_dto(entity)
    
    async def delete(self, id: T_ID) -> None:
        entity = await self.repository.get(id)
        if not entity:
            raise ValidationError.id_not_exists(id)
        await self.repository.delete(id)
        entity_name = entity.__class__.__name__
        self.logger.info(f"{entity_name} deleted with ID {entity.id}")
        return True

    async def list_all(self) -> List[TReadDTO]:
        entities = await self.repository.list_all()
        return [self.mapper.to_dto(entity) for entity in entities]
    
    async def get(self, id: T_ID) -> TReadDTO:
        entity = await self.repository.get(id)
        if not entity:
            raise ValidationError.id_not_exists(id)
        return self.mapper.to_dto(entity)      
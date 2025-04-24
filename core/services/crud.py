from ports.input.crud import CRUDPort
from core.services.default import DefaultService
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TUpdateDTO,
    TReadDTO,
    InternalData
)

class CRUDService(
    DefaultService[T_ID, TEntity, TCreateDTO, TReadDTO, InternalData],
    CRUDPort[T_ID, TCreateDTO, TReadDTO, TUpdateDTO]
):
    async def create(self, dto: TCreateDTO) -> TReadDTO:
        raw_data = self.mapper.to_internal_data(dto)

        hook = self.hooks.get("create", None)
        data = raw_data
        if hook and hook.has_before():
            data = await hook.run_before_hooks(raw_data)

        entity = self.mapper.from_internal_data(data)
        read_dto = await self._create(entity)

        if hook and hook.has_after():
            await hook.run_after_hooks(data)

        return read_dto

    async def _create(self, entity: TEntity) -> TReadDTO:
        saved = self.repository.save(entity)
        return self.mapper.to_dto(saved)

    async def update(self, id: T_ID, dto: TUpdateDTO) -> TReadDTO:
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")

        raw_data = self.mapper.to_internal_data(dto)

        hook = self.hooks.get("update", None)
        data = raw_data
        if hook and hook.has_before():
            data = await hook.run_before_hooks(raw_data)

        processed_entity = self.mapper.merge_changes(entity, data)
        dto = await self._update(processed_entity)

        if hook and hook.has_after():
            await hook.run_after_hooks(processed_entity)

        return dto

    async def _update(self, entity: TEntity) -> TReadDTO:
        saved = self.repository.save(entity)
        return self.mapper.to_dto(saved)

    async def delete(self, id: T_ID) -> bool:
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")

        data = self.mapper.from_entity_to_internal_data(entity)

        hook = self.hooks.get("delete", None)
        if hook and hook.has_before():
            data = await hook.run_before_hooks(data)

        self.repository.delete(id)

        if hook and hook.has_after():
            await hook.run_after_hooks(data)

        return True

    async def get(self, id: T_ID) -> TReadDTO:
        entity = self.repository.get(id)
        if entity is None:
            raise ValueError("Entity not found")
        return self.mapper.to_dto(entity)

    async def list_all(self) -> list[TReadDTO]:
        return [self.mapper.to_dto(e) for e in self.repository.list_all()]
from typing import List
from ports.input.crud import CRUDPort
from core.services.default import DefaultService
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TUpdateDTO,
    TReadDTO,
    TInternalData,
    PASIVE_DELETION_FLAG
)
from hooks.base import HookOrchestrator, BaseHook

class CRUDService(
    DefaultService[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData],
    CRUDPort[TCreateDTO, TReadDTO, TUpdateDTO, T_ID]
):
    async def create(self, dto: TCreateDTO) -> TReadDTO:
        raw_data = self.mapper.to_internal_data(dto)
        processed_data = await self._run_before_create_hooks(raw_data)
        entity = self.mapper.from_internal_data(processed_data)
        await self._persist(entity)
        
        read_dto = self.mapper.to_dto(entity, processed_data.get_context())
        await self._run_after_create_hooks(processed_data)
        return read_dto
    
    async def update(self, id: T_ID, dto: TUpdateDTO) -> TReadDTO:
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")
        
        raw_data = self.mapper.define_unset_fields_from_entity(entity, dto)
        processed_data = await self._run_before_update_hooks(raw_data)
        merged_entity = self.mapper.merge_changes(entity, processed_data)
        await self._persist(merged_entity)
        
        read_dto = self.mapper.to_dto(merged_entity, processed_data.get_context())
        await self._run_after_update_hooks(
            self.mapper.from_entity_to_internal_data(merged_entity)
        )
        return read_dto

    async def delete(self, id: T_ID) -> bool:
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")
        
        data = self.mapper.from_entity_to_internal_data(entity)
        processed_data = await self._run_before_delete_hooks(data)
        
        if self.__read_from_context(processed_data, PASIVE_DELETION_FLAG):
            await self._persist(self.mapper.from_internal_data(processed_data))
        else:
            self.repository.delete(id)
        
        await self._run_after_delete_hooks(processed_data)
        return True

    # TODO: Define the hooks and default behavior of get and list all methods.

    # async def get(self, id: T_ID) -> TReadDTO:
    #     entity = self.repository.get(id)
    #     if entity is None:
    #         raise ValueError("Entity not found")
    #     raw_data = self.mapper.from_entity_to_internal_data(entity)
    #     processed_data = await self._run_before_get_hooks(raw_data)
    #     read_dto = self.mapper.to_dto(entity, processed_data.get_context())
    #     await self._run_after_get_hooks(read_dto)
    #     return read_dto

    # async def list_all(self) -> list[TReadDTO]:
    #     all = [entity for entity in self.repository.list_all()]
    #     data = [self.mapper.from_entity_to_internal_data(entity) for 
    #             entity in all]
    #     processed_data = await self._run_after_list_hooks(data)
    #     list_of_dtos = [self.mapper.to_dto(entity, data.get_context()) for
    #                     entity, data in zip(all, processed_data)]
    #     await self._run_after_list_hooks(processed_data)
    #     return list_of_dtos

    def build_hook_orchestrator(self, hooks: BaseHook) -> HookOrchestrator:
        return HookOrchestrator.from_hooks(hooks)

    # Create
    async def _run_before_create_hooks(self, data: TInternalData) -> TInternalData:
        return data

    async def _run_after_create_hooks(self, data: TInternalData) -> TInternalData:
        return data

    # Update
    async def _run_before_update_hooks(self, data: TInternalData) -> TInternalData:
        return data

    async def _run_after_update_hooks(self, data: TInternalData) -> TInternalData:
        return data

    # Delete
    async def _run_before_delete_hooks(self, data: TInternalData) -> TInternalData:
        return data

    async def _run_after_delete_hooks(self, data: TInternalData) -> TInternalData:
        return data

    # Get
    async def _run_before_get_hooks(self, data: TInternalData) -> TInternalData:
        return data

    async def _run_after_get_hooks(self, data: TInternalData) -> TInternalData:
        return data

    # List
    async def _run_before_list_hooks(self, data: List[TInternalData]) -> List[TInternalData]:
        return data

    async def _run_after_list_hooks(self, data: List[TInternalData]) -> List[TInternalData]:
        return data
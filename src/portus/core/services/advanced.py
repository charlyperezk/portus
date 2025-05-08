from logging import Logger
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
    RELATION_SETTED_FLAG
)
from portus.hooks.base import HookOrchestrator, BaseHook

class AdvancedCRUDService(
    DefaultService[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData],
    CRUDPort[TCreateDTO, TReadDTO, TUpdateDTO, T_ID],
    Generic[TEntity, T_ID, TCreateDTO, TReadDTO, TInternalData, TUpdateDTO]
):
    async def create(self, dto: TCreateDTO) -> TReadDTO:
        raw_data = self.mapper.to_internal_data(dto)
        processed_data = await self._run_before_create_hooks(raw_data)
        entity = self.mapper.from_internal_data(processed_data)
        await self._persist(entity)

        entity_name = entity.__class__.__name__
        self.logger.info(f"{entity_name} created with ID {entity.id}")
        processed_data.print_trace(logger=self.log_debug, prefix="Create flow")
        
        read_dto = self.mapper.to_dto(
            entity,
            processed_data.get_flags_within_context(
                prefix=RELATION_SETTED_FLAG
            )
        )
        
        await self._run_after_create_hooks(processed_data)
        return read_dto
    
    async def update(self, id: T_ID, dto: TUpdateDTO) -> TReadDTO:
        entity = await self.repository.get(id)
        if not entity:
            raise ValidationError.id_not_exists(id)
        self.logger.debug(f"Detected changes {dto.model_dump(exclude_unset=True)}")
        raw_data = self.mapper.define_unset_fields_from_entity(entity, dto)
        processed_data = await self._run_before_update_hooks(raw_data)
        merged_entity = self.mapper.merge_changes(entity, processed_data)
        await self.repository.update(merged_entity)
        
        entity_name = entity.__class__.__name__
        self.logger.info(f"{entity_name} updated with ID {entity.id}")

        read_dto = self.mapper.to_dto(
            merged_entity,
            processed_data.get_flags_within_context(
                prefix=RELATION_SETTED_FLAG
            )
        )

        processed_data.print_trace(logger=self.log_debug, prefix="Update flow")

        await self._run_after_update_hooks(
            self.mapper.from_entity_to_internal_data(merged_entity)
        )
        return read_dto

    async def delete(self, id: T_ID) -> bool:
        entity = await self.repository.get(id)
        if not entity:
            raise ValidationError.id_not_exists(id)
        
        data = self.mapper.from_entity_to_internal_data(entity)
        processed_data = await self._run_before_delete_hooks(data)
        
        await self.repository.delete(id)

        processed_data.print_trace(logger=self.log_debug, prefix="Delete flow")

        await self._run_after_delete_hooks(processed_data)
        return True

    async def get(self, id: T_ID) -> TReadDTO:
        entity = await self.repository.get(id)
        if entity is None:
            raise ValidationError.id_not_exists(id)
        
        raw_data = self.mapper.from_entity_to_internal_data(entity)
        processed_data = await self._run_before_get_hooks(raw_data)
        
        read_dto = self.mapper.to_dto(
            entity,
            processed_data.get_flags_within_context(
                prefix=RELATION_SETTED_FLAG
            )
        )

        await self._run_after_get_hooks(read_dto)
        return read_dto

    async def list_all(self) -> list[TReadDTO]:
        all = await self.repository.list_all()
        data = [self.mapper.from_entity_to_internal_data(entity) for 
                entity in all]
        processed_data = await self._run_before_list_hooks(data)
        
        list_of_dtos = [self.mapper.to_dto(
            entity,
            data.get_flags_within_context(
                prefix=RELATION_SETTED_FLAG
            )
        ) for entity, data in zip(all, processed_data)]

        await self._run_after_list_hooks(processed_data)
        return list_of_dtos

    def build_hook_orchestrator(self, hooks: BaseHook, logger: Logger) -> HookOrchestrator:
        return self.hook_orchestrator_cls.from_hooks(hooks, logger)

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
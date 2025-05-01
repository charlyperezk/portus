from logging import Logger
from typing import List
from ports.input.crud import CRUDPort
from core.services.default import DefaultService
from common.exceptions import ValidationError
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TUpdateDTO,
    TReadDTO,
    TInternalData,
    PASSIVE_DELETION_FLAG,
    RELATION_SETTED_FLAG
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
            raise ValidationError.id_not_exists(f"Entity with ID {id} not found.")
        
        raw_data = self.mapper.define_unset_fields_from_entity(entity, dto)
        processed_data = await self._run_before_update_hooks(raw_data)
        merged_entity = self.mapper.merge_changes(entity, processed_data)
        await self._persist(merged_entity)
        
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
            raise ValidationError.id_not_exists(f"Entity with ID {id} not found.")
        
        data = self.mapper.from_entity_to_internal_data(entity)
        processed_data = await self._run_before_delete_hooks(data)
        
        entity_name = entity.__class__.__name__
        
        if processed_data.get_flags_within_context(
            prefix=PASSIVE_DELETION_FLAG
        ):
            await self._persist(self.mapper.from_internal_data(processed_data))
            self.logger.info(f"{entity_name} was soft-deleted with ID {entity.id}")
        else:
            self.repository.delete(id)
            self.logger.info(f"{entity_name} was hard-deleted with ID {entity.id}")

        processed_data.print_trace(logger=self.log_debug, prefix="Delete flow")

        await self._run_after_delete_hooks(processed_data)
        return True

    async def get(self, id: T_ID) -> TReadDTO:
        entity = await self.repository.get(id)
        if entity is None:
            raise ValidationError.id_not_exists(f"Entity with ID {id} not found.")
        
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
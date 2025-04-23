from typing import Literal, Union, Optional

from ports.input.crud import CRUDPort
from ports.output.repository import CrudRepository, RelationRepository
from hooks.base.life_cycle import LifeCycle
from mappers.base import Mapper
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TUpdateDTO,
    TReadDTO,
    TInternalData
)

HooksMap = dict[Literal["create", "update", "delete"], LifeCycle]
RelatedRepository = dict[str, RelationRepository[T_ID, Union[int, str]]]

class Service(CRUDPort[TCreateDTO, TReadDTO, T_ID, TUpdateDTO]):
    """
    Generic base service for CRUD operations with support for:
    - Persistent storage via repository
    - Mapping between DTOs and entities
    - Validation and transformation hooks (before/after)
    - Related repositories for external reference checks
    """

    def __init__(
        self,
        repository: CrudRepository[TEntity, T_ID],
        mapper: Mapper[TEntity, TReadDTO, TCreateDTO, TInternalData],
        related_repositories: RelatedRepository = None,
        hooks: Optional[HooksMap] = None
,
    ):
        self.repository = repository  # Main entity persistence layer
        self.mapper = mapper  # Converts between DTOs, entities, and internal data
        self.related_repositories = related_repositories or {}  # For validating related entities
        self.hooks = hooks or {} # Lifecycle hooks for create/update/delete stages

    async def create(self, dto: TCreateDTO) -> TReadDTO:
        raw_data = self.mapper.to_internal_data(dto)

        # Run 'before' hooks for validations and transformations
        hook = self.hooks.get("create", None)
        data = raw_data
        if hook and hook.has_before():
            data = await hook.run_before_hooks(raw_data)

        # Convert processed data to entity and persist it
        entity = self.mapper.from_internal_data(data)
        dto = await self._create(entity)

        # Run 'after' hooks (e.g., send events)
        if hook and hook.has_after():
            await hook.run_after_hooks(data)

        return dto

    async def _create(self, entity: TEntity) -> TReadDTO:
        # Save entity and convert to read DTO
        saved = self.repository.save(entity)
        return self.mapper.to_dto(saved)

    async def update(self, id: T_ID, dto: TUpdateDTO) -> TReadDTO:
        # Retrieve existing entity or raise error if not found
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")

        raw_data = self.mapper.to_internal_data(dto)

        # Run 'before' hooks for validations and transformations
        hook = self.hooks.get("update", None)
        data = raw_data
        if hook and hook.has_before():
            data = await hook.run_before_hooks(raw_data)

        # Merge changes and update entity
        processed_entity = self.mapper.merge_changes(entity, data)
        dto = await self._update(processed_entity)

        # Run 'after' hooks (e.g., emit domain events)
        if hook and hook.has_after():
            await hook.run_after_hooks(processed_entity)

        return dto

    async def _update(self, entity: TEntity) -> TReadDTO:
        # Save updated entity and return DTO
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

        processed_entity = self.mapper.merge_changes(entity, data) 
        await self._delete(processed_entity)        

        if hook and hook.has_after():
            await hook.run_after_hooks(processed_entity)

        return True

    async def _delete(self, entity: TEntity) -> bool:
        self.repository.save(entity)
    
    async def get(self, id: T_ID) -> TReadDTO:
        entity = self.repository.get(id)
        if entity is None or not entity.active:
            raise ValueError("Entity not found")
        return self.mapper.to_dto(entity)

    async def list_all(self) -> list[TReadDTO]:
        return [self.mapper.to_dto(e) for e in self.repository.list_all() if e.active]

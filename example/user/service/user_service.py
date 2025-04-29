"""
TODO: Implement delete, get and list_all methods and integration tests with hooks if necessary.
"""

from mappers import DefaultMapper
from common.types import InternalData
from core.services import CRUDService
from example.user.repositories import UserInMemoryRepository, CountryRelationRepository
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from example.user.entities import User

from example.user.service.methods.create import (
    get_create_validation_hooks,
    get_create_transformation_hooks,
    get_create_trigger_hooks
)

from example.user.service.methods.update import (
    get_update_validation_hooks,
    get_update_transformation_hooks,
    get_update_trigger_hooks
)

class UserService(CRUDService[str, User, UserCreateDTO, UserReadDTO, InternalData, UserUpdateDTO]):
    def __init__(self):
        super().__init__(
            repository=UserInMemoryRepository(),
            mapper=DefaultMapper(User, UserReadDTO, InternalData),
            related_repositories={
                "country_id": CountryRelationRepository()
            }
        )

    # async def delete(self, id: str) -> bool:
    #     entity = self.repository.get(id)
    #     if not entity:
    #         raise ValueError(f"Entity with ID {id} not found.")

    #     raw_data = self.mapper.from_entity_to_internal_data(entity)
    #     processed_data = await self._run_before_delete_hooks(raw_data)
    #     merged_entity = self.mapper.merge_changes(entity, processed_data) 
    #     await self._persist(merged_entity)
    #     await self._run_after_delete_hooks(processed_data)
    #     return True
    
    # async def get(self, id: str) -> UserReadDTO:
    #     entity = self.repository.get(id)
    #     if entity is None or not entity.active:
    #         raise ValueError("Entity not found")
    #     raw_data = self.mapper.from_entity_to_internal_data(entity)
    #     processed_data = await self._run_before_get_hooks(raw_data)
    #     read_dto = self.mapper.to_dto(entity, processed_data.get_context())
    #     await self._run_after_get_hooks(read_dto)
    #     return read_dto

    # async def list_all(self) -> list[UserReadDTO]:
    #     all = [entity for entity in self.repository.list_all() if entity.active]
    #     data = [self.mapper.from_entity_to_internal_data(entity) for 
    #             entity in all]
    #     processed_data = await self._run_after_list_hooks(data)
    #     list_of_dtos = [self.mapper.to_dto(entity, data.get_context()) for
    #                     entity, data in zip(all, processed_data)]
    #     await self._run_after_list_hooks(processed_data)
    #     return list_of_dtos

    async def _run_before_create_hooks(self, data: InternalData) -> InternalData:
        validations = self.build_hook_orchestrator(
            get_create_validation_hooks(
                user_repository=self.repository,
                country_repository=self.related_repositories["country_id"]
            )
        )
        await validations.run(data)
        transformations = self.build_hook_orchestrator(
            get_create_transformation_hooks(country_repository=self.related_repositories["country_id"])
        )
        return await transformations.run(data)

    async def _run_after_create_hooks(self, data: InternalData) -> InternalData:
        triggers = self.build_hook_orchestrator(get_create_trigger_hooks())
        await triggers.run(data)

    async def _run_before_update_hooks(self, data: InternalData) -> InternalData:
        validations = self.build_hook_orchestrator(
            get_update_validation_hooks(
                user_repository=self.repository,
                country_repository=self.related_repositories["country_id"]
            )
        )
        await validations.run(data)
        transformations = self.build_hook_orchestrator(
            get_update_transformation_hooks(country_repository=self.related_repositories["country_id"])
        )
        return await transformations.run(data)

    async def _run_after_update_hooks(self, data: InternalData) -> InternalData:
        triggers = self.build_hook_orchestrator(get_update_trigger_hooks())
        await triggers.run(data)
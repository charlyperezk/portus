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

from example.user.service.methods.delete import (
    get_delete_transformation_hooks,
    get_delete_trigger_hooks
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

    async def _run_before_create_hooks(self, data: InternalData) -> InternalData:
        validations = self.build_hook_orchestrator(
            get_create_validation_hooks(
                user_repository=self.repository,
                country_repository=self.related_repositories["country_id"]
            )
        )
        await validations.run(data)
        transformations = self.build_hook_orchestrator(
            get_create_transformation_hooks(
                country_repository=self.related_repositories["country_id"]
            )
        )
        return await transformations.run(data)

    async def _run_after_create_hooks(self, data: InternalData) -> None:
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
            get_update_transformation_hooks(
                country_repository=self.related_repositories["country_id"]
            )
        )
        return await transformations.run(data)

    async def _run_after_update_hooks(self, data: InternalData):
        triggers = self.build_hook_orchestrator(get_update_trigger_hooks())
        await triggers.run(data)

    async def _run_before_delete_hooks(self, data: InternalData) -> InternalData:
        transformations = self.build_hook_orchestrator(
            get_delete_transformation_hooks()
        )
        return await transformations.run(data)
    
    async def _run_after_delete_hooks(self, data: InternalData):
        triggers = self.build_hook_orchestrator(get_delete_trigger_hooks())
        await triggers.run(data)
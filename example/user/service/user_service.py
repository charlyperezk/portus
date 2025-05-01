from typing import List
from mappers import DefaultMapper
from common.types import InternalData
from core.services import CRUDService
from hooks.base.orchestrator import HookOrchestrator

from example.user.config import service_logger, orchestrator_logger
from example.user.repositories import UserInMemoryRepository, CountryRelationRepository
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from example.user.entities import User
from example.user.service.methods.create import (
    create_validation_hooks,
    create_transformation_hooks,
    create_trigger_hooks
)

from example.user.service.methods.update import (
    update_validation_hooks,
    update_transformation_hooks,
    update_trigger_hooks
)

from example.user.service.methods.delete import (
    delete_transformation_hooks,
    delete_trigger_hooks
)

from example.user.service.methods.get import (
    get_transformation_hooks
)

class UserService(CRUDService[str, User, UserCreateDTO, UserReadDTO, InternalData, UserUpdateDTO]):
    def __init__(self):
        super().__init__(
            repository=UserInMemoryRepository(),
            mapper=DefaultMapper(User, UserReadDTO, InternalData),
            related_repositories={
                "country_id": CountryRelationRepository()
            },
            logger=service_logger,
            hook_orchestrator_cls=HookOrchestrator(logger=orchestrator_logger)
        )

    async def _run_hooks(self, step: str, action: str, data: InternalData) -> InternalData | None:
        hook_getters = {
            "create": {
                "validation": lambda: create_validation_hooks(self.repository, self.related_repositories["country_id"]),
                "transformation": lambda: create_transformation_hooks(self.related_repositories["country_id"]),
                "trigger": create_trigger_hooks
            },
            "update": {
                "validation": lambda: update_validation_hooks(self.repository, self.related_repositories["country_id"]),
                "transformation": lambda: update_transformation_hooks(self.related_repositories["country_id"]),
                "trigger": update_trigger_hooks
            },
            "delete": {
                "transformation": delete_transformation_hooks,
                "trigger": delete_trigger_hooks
            },
            "get": {
                "transformation": lambda: get_transformation_hooks(self.related_repositories["country_id"])
            }

        }

        hooks = hook_getters[action][step]()
        orchestrator = self.build_hook_orchestrator(hooks=hooks, logger=orchestrator_logger)

        if step in ("validation", "transformation"):
            return await orchestrator.run(data, step)
        else:
            await orchestrator.run(data, "trigger")

    async def _run_before_create_hooks(self, data: InternalData) -> InternalData:
        self.log_info("Create flow - running validation hooks ...")
        data = await self._run_hooks("validation", "create", data)
        self.log_info("Create flow - running transformation hooks ...")
        return await self._run_hooks("transformation", "create", data)
    
    async def _run_after_create_hooks(self, data: InternalData):
        self.log_info("Create flow - running triggered hooks ...")
        await self._run_hooks("trigger", "create", data)

    async def _run_before_update_hooks(self, data: InternalData) -> InternalData:
        self.log_info("Update flow - running validation hooks ...")
        data = await self._run_hooks("validation", "update", data)
        self.log_info("Update flow - running transformation hooks ...")
        return await self._run_hooks("transformation", "update", data)

    async def _run_after_update_hooks(self, data: InternalData):
        self.log_info("Update flow - running triggered hooks ...")
        await self._run_hooks("trigger", "update", data)

    async def _run_before_delete_hooks(self, data: InternalData) -> InternalData:
        self.log_info("Delete flow - running transformation hooks ...")
        return await self._run_hooks("transformation", "delete", data)

    async def _run_after_delete_hooks(self, data: InternalData):
        self.log_info("Delete flow - running triggered hooks ...")
        await self._run_hooks("trigger", "delete", data)

    async def _run_before_get_hooks(self, data: InternalData) -> InternalData:
        self.log_info("Get flow - running transformation hooks ...")
        return await self._run_hooks("transformation", "get", data)

    async def _run_after_get_hooks(self, data):
        return await super()._run_after_get_hooks(data)
    
    async def _run_before_list_hooks(self, data: List[InternalData]) -> List[InternalData]:
        self.log_info("List all flow - running transformation hooks ...")    
        processed_data = []
        for d in data:
            result = await self._run_hooks("transformation", "get", d)
            processed_data += [result]
        return processed_data

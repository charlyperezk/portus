from portus.common.logger import Logger, create_logger
from typing import Dict, Union, Optional, Generic
from portus.ports.output.repository import CrudRepository, GetAndAskRepository
from portus.hooks.base import HookOrchestrator
from portus.mappers.base import Mapper
from portus.common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TReadDTO,
    TInternalData,
)

RelatedRepository = Dict[str, GetAndAskRepository[T_ID, Union[int, str]]]

class DefaultService(Generic[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData]):
    def __init__(
        self,
        repository: CrudRepository[T_ID, TEntity],
        mapper: Mapper[TEntity, TCreateDTO, TReadDTO, TInternalData],
        related_repositories: Optional[RelatedRepository] = None,
        logger: Optional[Logger] = None,
        hook_orchestrator_cls: Optional[HookOrchestrator] = None
    ):
        self.repository = repository  # Main entity persistence layer
        self.mapper = mapper  # Converts between DTOs, entities, and internal data
        self.related_repositories = related_repositories or {}  # For validating related entities
        self.logger = logger or create_logger("Service")
        self.hook_orchestrator_cls = hook_orchestrator_cls or HookOrchestrator

        self.log_info("Initialized")

    async def _persist(self, object: TEntity) -> TReadDTO:
        return await self.repository.save(object)

    def log_info(self, message: str) -> None:
        self.logger.info(message)

    def log_debug(self, message: str) -> None:
        self.logger.debug(message)

    def log_error(self, message: str) -> None:
        self.logger.error(message)

    def log_error(self, message: str) -> None:
        self.logger.warning(message)

from typing import Dict, Union, Optional, Generic

from ports.output.repository import CrudRepository, GetAndAskRepository
from mappers.base import Mapper
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TReadDTO,
    TInternalData,
)

class DefaultService(Generic[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData]):
    def __init__(
        self,
        repository: CrudRepository[T_ID, TEntity],
        mapper: Mapper[TEntity, TCreateDTO, TReadDTO, TInternalData],
        related_repositories: Optional[Dict[str, GetAndAskRepository[T_ID, Union[int, str]]]] = None,
    ):
        self.repository = repository  # Main entity persistence layer
        self.mapper = mapper  # Converts between DTOs, entities, and internal data
        self.related_repositories = related_repositories or {}  # For validating related entities

    async def _persist(self, object: TEntity) -> TReadDTO:
        return self.repository.save(object)
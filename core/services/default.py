from typing import Literal, Union, Optional, Generic

from ports.output.repository import CrudRepository, GetAndAskRepository
from hooks.base.life_cycle import LifeCycle
from mappers.base import Mapper
from common.types import (
    T_ID,
    TEntity,
    TCreateDTO,
    TReadDTO,
    TInternalData
)

RelationRepository = GetAndAskRepository
HooksMap = dict[Literal["create", "update", "delete"], LifeCycle]
RelatedRepository = dict[str, RelationRepository[T_ID, Union[int, str]]]

class DefaultService(Generic[T_ID, TEntity, TCreateDTO, TReadDTO, TInternalData]):
    def __init__(
        self,
        repository: CrudRepository[T_ID, TEntity],
        mapper: Mapper[TEntity, TCreateDTO, TReadDTO, TInternalData],
        related_repositories: Optional[RelatedRepository] = None,
        hooks: Optional[HooksMap] = None
,
    ):
        self.repository = repository  # Main entity persistence layer
        self.mapper = mapper  # Converts between DTOs, entities, and internal data
        self.related_repositories = related_repositories or {}  # For validating related entities
        self.hooks = hooks or {} # Lifecycle hooks for create/update/delete stages
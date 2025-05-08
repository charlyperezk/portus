from typing import Type, Optional, Generic
from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClient
from portus.common.types import T_ID, TEntity, TDBModel
from portus.common.logger import Logger
from portus.mappers.db_base import DBMapper
from portus.common.exceptions import EntityNotFoundException, RepositoryException
from portus.ports.output.repository import GetAndAskRepository

DBMapperType = DBMapper[TDBModel, TEntity]

class RelationBeanieAsyncRepository(
    GetAndAskRepository[T_ID, TEntity],
    Generic[T_ID, TEntity],
):
    def __init__(
        self,
        model: Type[Document],
        mapper: Type[DBMapperType],
        logger: Optional[Logger] = None
    ):
        self.model = model
        self.mapper = mapper
        self.logger = logger or Logger(__name__)

    async def get(self, entity_id: T_ID) -> Optional[TEntity]:
        try:
            model = await self.model.get(entity_id)
            if not model:
                self.logger.warning(f"Entity with ID {entity_id} not found")
                raise EntityNotFoundException(entity_id)
            self.logger.info(f"Entity found: {model}")
            return self.mapper.from_model(model)
        except Exception as e:
            self.logger.error(f"Error reading entity: {e}")
            raise RepositoryException(str(e))

    async def exists(self, entity_id: T_ID) -> bool:
        try:
            model = await self.model.get(entity_id)
            found = model is not None
            self.logger.debug(f"Entity {entity_id} exists: {found}")
            return found
        except Exception as e:
            self.logger.error(f"Error checking existence: {e}")
            raise RepositoryException(str(e))

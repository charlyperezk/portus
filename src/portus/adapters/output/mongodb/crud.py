from typing import Type, Generic, Optional, List
from beanie import Document
from pymongo.errors import PyMongoError
from portus.common.types import T_ID, TEntity, TDBModel
from portus.common.logger import Logger
from portus.common.exceptions import EntityNotFoundException, RepositoryException
from portus.ports.output.repository import CrudRepository
from portus.mappers.db_base import DBMapper
from portus.adapters.output.mongodb.related import RelationBeanieAsyncRepository

DBMapperType = DBMapper[TDBModel, TEntity]

class CRUDBeanieAsyncAdapter(
    RelationBeanieAsyncRepository[T_ID, TEntity],
    CrudRepository[T_ID, TEntity],
    Generic[T_ID, TEntity, TDBModel]
):
    def __init__(
        self,
        model_cls: Type[Document],
        mapper: Type[DBMapperType],
        logger: Optional[Logger] = None,
    ):
        super().__init__(model_cls, mapper, logger)
        self.model_cls = model_cls
        self.mapper = mapper
        self.logger = logger or Logger(__name__)

    def to_model(self, entity: TEntity) -> TDBModel:
        return self.mapper.to_model(entity)

    def from_model(self, model: TDBModel) -> TEntity:
        return self.mapper.from_model(model)

    async def save(self, entity: TEntity) -> TEntity:
        model = self.to_model(entity)
        try:
            await model.create()
            self.logger.info(f"Entity created: {model}")
            return self.from_model(model)

        except Exception as e:
            self.logger.error(f"Error creating entity: {e}")
            raise RepositoryException(f"Error creating entity: {e}")

    async def list_all(self) -> List[TEntity]:
        try:
            models = await self.model_cls.find_all().to_list()
            self.logger.info(f"All entities retrieved: {models}")
            return [self.from_model(m) for m in models]

        except Exception as e:
            self.logger.error(f"Error listing entities: {e}")
            raise RepositoryException(f"Error listing entities: {e}")

    async def update(self, entity: TEntity) -> TEntity:
        model = self.to_model(entity)
        try:
            existing = await self.model_cls.get(model.id)
            if not existing:
                raise EntityNotFoundException(model.id)

            await model.replace()
            self.logger.info(f"Entity updated: {model}")
            return self.from_model(model)

        except Exception as e:
            self.logger.error(f"Error updating entity: {e}")
            raise RepositoryException(f"Error updating entity: {e}")

    async def delete(self, entity_id: T_ID) -> bool:
        try:
            model = await self.model_cls.get(entity_id)
            if not model:
                raise EntityNotFoundException(entity_id)
            await model.delete()
            self.logger.info(f"Entity with ID {entity_id} deleted")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting entity: {e}")
            raise RepositoryException(f"Error deleting entity: {e}")
from typing import Type, Generic, Optional, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from portus.mappers.db_base import DBMapper
from portus.common.types import T_ID, TEntity, TDBModel
from portus.common.logger import Logger
from portus.common.exceptions import EntityNotFoundException, RepositoryException
from portus.ports.output.repository import CrudRepository
from portus.adapters.output.sqlalchemy.related import RelationSQLAlchemyAsyncRepository

DBMapperType = DBMapper[TDBModel, TEntity]

class CRUDSQLAlchemyAsyncAdapter(
    RelationSQLAlchemyAsyncRepository[T_ID, TEntity],
    CrudRepository[T_ID, TEntity],
    Generic[T_ID, TEntity]
):
    def __init__(
        self,
        db_url: str,
        mapper: Type[DBMapperType],
        logger: Optional[Logger] = None,
    ):
        super().__init__(db_url, mapper, logger)
        self.mapper = mapper
        self.logger = logger or Logger(__name__)

    def to_model(self, entity: TEntity) -> TDBModel:
        return self.mapper.to_model(entity)

    def from_model(self, model: TDBModel) -> TEntity:
        return self.mapper.from_model(model)

    def get_table_name(self) -> str:
        return self.mapper.get_table_name()

    def assign_id(self):
        pass

    async def save(self, entity: TEntity) -> TEntity:
        model = self.to_model(entity)
        async with self.get_session() as session:
            try:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                self.logger.info(f"Entity created: {model}")
                return self.from_model(model)
            
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Error creating entity: {e.__cause__}")
                raise RepositoryException(f"Error creating entity: {e.__cause__}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")

    async def list_all(self) -> List[TEntity]:
        async with self.get_session() as session:
            try:
                result = await session.execute(select(self.mapper.get_model_class()))
                models = result.scalars().all()
                self.logger.info(f"All entities retrieved: {models}")
                return [self.from_model(model) for model in models]
            
            except SQLAlchemyError as e:
                self.logger.error(f"Error listing entities: {e.__cause__}")
                raise RepositoryException(f"Error listing entities: {e.__cause__}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")

    async def update(self, entity: TEntity) -> TEntity:
        model = self.to_model(entity)
        async with self.get_session() as session:
            try:
                await session.merge(model)
                await session.commit()
                self.logger.info(f"Entity updated: {model}")
                return self.from_model(model)
            
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Error updating entity: {e.__cause__}")
                raise RepositoryException(f"Error updating entity: {e.__cause__}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")

    async def delete(self, entity_id: T_ID) -> bool:
        async with self.get_session() as session:
            try:
                model = await session.get(self.mapper.get_model_class(), entity_id)
                if model:
                    await session.delete(model)
                    await session.commit()
                    self.logger.info(f"Entity with ID {entity_id} deleted")
                    return True
                else:
                    self.logger.warning(f"Entity with ID {entity_id} not found")
                    raise EntityNotFoundException(entity_id)
                
            except SQLAlchemyError as e:
                await session.rollback()
                self.logger.error(f"Error deleting entity: {e.__cause__}")
                raise RepositoryException(f"Error deleting entity: {e.__cause__}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")
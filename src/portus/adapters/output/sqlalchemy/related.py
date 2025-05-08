from typing import Generic, Type, Optional
from sqlalchemy.exc import SQLAlchemyError
from portus.common.types import T_ID, TDBModel, TEntity
from portus.common.logger import Logger
from portus.common.exceptions import EntityNotFoundException, RepositoryException
from portus.mappers.db_base import DBMapper
from portus.adapters.output.sqlalchemy import SQLAlchemyAsyncAdapter
from portus.ports.output.repository import GetAndAskRepository

class RelationSQLAlchemyAsyncRepository(
    SQLAlchemyAsyncAdapter,
    GetAndAskRepository[T_ID, TEntity],
    Generic[T_ID, TEntity],
):
    def __init__(
        self,
        db_url: str,
        mapper: Type[DBMapper[TDBModel, TEntity]],
        logger: Optional[Logger] = None,
    ):
        super().__init__(db_url, logger)
        self.mapper = mapper
        self.logger = logger or Logger(__name__)

    async def get(self, entity_id: T_ID) -> Optional[TEntity]:
        async with self.get_session() as session:
            try:
                model = await session.get(self.mapper.get_model_class(), entity_id)
                if model:
                    self.logger.info(f"Entity found: {model}")
                    return self.mapper.from_model(model)
                else:
                    self.logger.warning(f"Entity with ID {entity_id} not found")
                    raise EntityNotFoundException(entity_id)
            
            except SQLAlchemyError as e:
                self.logger.error(f"Error reading entity: {e.__cause__}")
                raise RepositoryException(f"Error reading entity: {e.__cause__}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")

    async def exists(self, id: T_ID) -> bool:
        async with self.get_session() as session:
            try:
                obj = await session.get(self.mapper.get_model_class(), id)
                found = obj is not None
                if found:
                    self.logger.debug(f"Entity {id} exists in {self.mapper.get_table_name()}")
                else:
                    self.logger.warning(f"Entity {id} does not exist in {self.mapper.get_table_name()}")
                    raise EntityNotFoundException(id)
                return found
            
            except SQLAlchemyError as e:
                self.logger.error(f"Error checking existence of {id}: {e}")
                raise Exception(f"Error checking existence of {id}: {e}")
            
            finally:
                await session.close()
                self.logger.debug("Session closed")
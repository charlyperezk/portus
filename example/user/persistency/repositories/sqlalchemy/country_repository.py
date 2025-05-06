import os
from example.user.entities import Country
from example.user.persistency.models import CountryDBModel
from example.user.config.loggers import related_repository_logger
from src.adapters.output.sqlalchemy.related import RelationSQLAlchemyAsyncRepository
from src.mappers.db_default import DefaultDBMapper

mapper = DefaultDBMapper(CountryDBModel, Country)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

class CountryRelationRepository(RelationSQLAlchemyAsyncRepository[Country, int]):
    def __init__(self):
        super().__init__(
            db_url=DATABASE_URL,
            mapper=mapper,
            logger=related_repository_logger
        )
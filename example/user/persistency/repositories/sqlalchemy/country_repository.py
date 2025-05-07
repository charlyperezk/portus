import os
from example.user.entities import Country
from example.user.persistency.models import CountryDBModel
from example.user.config.loggers import related_repository_logger
from example.user.persistency.repositories.sqlalchemy.config import DATABASE_URL
from src.adapters.output.sqlalchemy.related import RelationSQLAlchemyAsyncRepository
from src.mappers.db_default import DefaultDBMapper

mapper = DefaultDBMapper(CountryDBModel, Country)

class CountryRelationRepository(RelationSQLAlchemyAsyncRepository[Country, int]):
    def __init__(self):
        super().__init__(
            db_url=DATABASE_URL,
            mapper=mapper,
            logger=related_repository_logger
        )
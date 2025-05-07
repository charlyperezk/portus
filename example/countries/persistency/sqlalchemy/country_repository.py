import os
from example.countries.entities import Country
from example.countries.persistency.models import CountryDBModel
from example.countries.config.loggers import repository_logger
from example.countries.persistency.sqlalchemy.config import DATABASE_URL
from src.adapters.output.sqlalchemy.crud import CRUDSQLAlchemyAsyncAdapter
from src.mappers.db_default import DefaultDBMapper

mapper = DefaultDBMapper(CountryDBModel, Country)

class CountryRepository(CRUDSQLAlchemyAsyncAdapter[int, Country]):
    def __init__(self):
        super().__init__(
            db_url=DATABASE_URL,
            mapper=mapper,
            logger=repository_logger,
        )
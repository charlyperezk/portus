import os
from example.countries.entities import Country
from example.countries.persistency.models import CountryDBModel
from example.countries.config.loggers import repository_logger
from src.adapters.output.sqlalchemy.crud import CRUDSQLAlchemyAsyncAdapter
from src.mappers.db_default import DefaultDBMapper

mapper = DefaultDBMapper(CountryDBModel, Country)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

class CountryRepository(CRUDSQLAlchemyAsyncAdapter[int, Country]):
    def __init__(self):
        super().__init__(
            db_url=DATABASE_URL,
            mapper=mapper,
            logger=repository_logger,
        )
from typing import Optional, Callable
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

from portus.common.logger import Logger, create_logger

Base = declarative_base()

async def create_all_tables(db_url: str):
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

class SQLAlchemyAsyncAdapter:
    def __init__(self, db_url: str, logger: Optional[Logger] = None):
        self.engine = create_async_engine(db_url, echo=False, future=True)
        self.Session: Callable[[], AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.logger = logger or create_logger("SQLAlchemyAsyncAdapter")

    def get_session(self) -> AsyncSession:
        return self.Session()

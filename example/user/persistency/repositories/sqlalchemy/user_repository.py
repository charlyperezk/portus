import os
from example.user.entities import User
from example.user.persistency.models import UserDBModel
from example.user.config.loggers import repository_logger
from src.portus.adapters.output.sqlalchemy.crud import CRUDSQLAlchemyAsyncAdapter
from src.portus.mappers.db_default import DefaultDBMapper
from src.portus.ports.output.repository.repository import GetByEmailPort

mapper = DefaultDBMapper(UserDBModel, User)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/portus.db") # Delete default value in production

class UserRepository(CRUDSQLAlchemyAsyncAdapter[str, User], GetByEmailPort[User]):
    def __init__(self):
        super().__init__(
            db_url=DATABASE_URL,
            mapper=mapper,
            logger=repository_logger,  # Replace with an actual logger instance
        )

    async def get(self, id: str) -> User:
        user = await super().get(id)
        if user and not user.active:
            return None
        return user
    
    async def list_all(self):
        users = await super().list_all()
        return [user for user in users if user.active]

    async def find_by_email(self, email: str):
        users = await self.list_all()
        email_coincidences_in_repo = [user for user in users if user.email == email]
        if any(email_coincidences_in_repo):
            return email_coincidences_in_repo[0]
        return None
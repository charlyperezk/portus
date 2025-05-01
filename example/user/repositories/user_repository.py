from example.user.entities import User
from typing import Optional
from ports.output.repository.repository import GetByEmailPort
from adapters.output.in_memory import InMemoryRepository

class UserInMemoryRepository(InMemoryRepository[User, str], GetByEmailPort[User]):
    async def find_by_email(self, email: str):
        entities = await self.list_all()
        email_coincidences_in_repo = [user for user in entities if user.email == email]
        if any(email_coincidences_in_repo):
            return email_coincidences_in_repo[0]
        return None
    
    async def soft_delete(self, entity: User) -> bool:
        if entity.active:
            raise ValueError("You must change to active=False")
        await self.save(entity)
        return True

    async def get(self, id: str) -> Optional[User]:
        user = await super().get(id)
        if user and not user.active:
            return None
        return user
    
    async def list_all(self):
        users = await super().list_all()
        return [user for user in users if user.active]
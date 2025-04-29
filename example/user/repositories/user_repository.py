from example.user.entities import User
from ports.output.repository.repository import GetByEmailPort
from adapters.output.in_memory import InMemoryRepository

class UserInMemoryRepository(InMemoryRepository[str, User], GetByEmailPort[User]):
    async def find_by_email(self, email: str):
        email_coincidences_in_repo = [user for user in self.list_all() if user.email == email]
        if any(email_coincidences_in_repo):
            return email_coincidences_in_repo[0]
        return None
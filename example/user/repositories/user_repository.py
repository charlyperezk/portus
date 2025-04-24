from example.user.entities import User
from adapters.output.in_memory import InMemoryRepository

class UserInMemoryRepository(InMemoryRepository[User, str]):
    ...
from example.user.entities import User
from adapters.output.in_memory import InMemoryRep

class UserInMemoryRepository(InMemoryRep[User, str]):
    ...
from adapters.output.in_memory import InMemoryRep
from mappers import DefaultMapper
from core.services.default import Service
from common.types import InternalData
from example.user.service import hooks
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from example.user.entities import User
from example.user.service.hooks import user_hooks

class UserService(Service[UserCreateDTO, UserReadDTO, str, UserUpdateDTO]):
    def __init__(self):
        super().__init__(
            repository=InMemoryRep(),
            mapper=DefaultMapper(User, UserReadDTO, InternalData),
            hooks=user_hooks
        )
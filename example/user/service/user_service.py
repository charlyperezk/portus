from mappers import DefaultMapper
from core.services.default import Service
from common.types import InternalData
from example.user.repositories import UserInMemoryRepository, CountryRelationRepository
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from example.user.entities import User
from example.user.service.hooks import user_hooks

class UserService(Service[UserCreateDTO, UserReadDTO, str, UserUpdateDTO]):
    def __init__(self):
        super().__init__(
            repository=UserInMemoryRepository(),
            mapper=DefaultMapper(User, UserReadDTO, InternalData),
            hooks=user_hooks,
            related_repositories={
                "country_id": CountryRelationRepository()
            }
        )
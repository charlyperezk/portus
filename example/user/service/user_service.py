from mappers import DefaultMapper
from core.services import CRUDService
from common.types import InternalData
from example.user.repositories import UserInMemoryRepository, CountryRelationRepository
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO
from example.user.entities import User
from example.user.service.hooks import user_hooks

class UserService(CRUDService[User, str, UserCreateDTO, UserReadDTO, UserUpdateDTO]):
    def __init__(self):
        super().__init__(
            repository=UserInMemoryRepository(),
            mapper=DefaultMapper(User, UserReadDTO, InternalData),
            hooks=user_hooks,
            related_repositories={
                "country_id": CountryRelationRepository()
            }
        )

    async def delete(self, id: str) -> bool:
        entity = self.repository.get(id)
        if not entity:
            raise ValueError(f"Entity with ID {id} not found.")

        data = self.mapper.from_entity_to_internal_data(entity)

        hook = self.hooks.get("delete", None)
        if hook and hook.has_before():
            data = await hook.run_before_hooks(data)

        processed_entity = self.mapper.merge_changes(entity, data) 
        await self._delete(processed_entity)        

        if hook and hook.has_after():
            await hook.run_after_hooks(processed_entity)

        return True
    
    async def _delete(self, entity: User) -> bool:
        self.repository.save(entity)

    async def get(self, id: str) -> UserReadDTO:
        user = self.repository.get(id)
        if user is None or not user.active:
            raise ValueError("user not found")
        return self.mapper.to_dto(user)

    async def list_all(self) -> list[UserReadDTO]:
        return [self.mapper.to_dto(user) for user in self.repository.list_all() if user.active]

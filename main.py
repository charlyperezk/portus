from typing import Optional
from example.user.service import UserService
from example.user.dtos import UserCreateDTO, UserUpdateDTO, UserReadDTO

async def create_user(service: UserService, dto: UserCreateDTO) -> UserReadDTO:
    return await service.create(dto)

async def update_user(service: UserService, id: str, dto: UserUpdateDTO) -> UserReadDTO:
    return await service.update(id, UserUpdateDTO(username="Charles"))

async def delete_user(service: UserService, id: str) -> bool:
    return await service.delete(id)

async def list_all_users(service: UserService) -> list[Optional[UserReadDTO]]:
    return await service.list_all()

async def get_user(service: UserService, id: str) -> UserReadDTO:
    return await service.get(id)

if __name__ == "__main__":
    """
        I'm using a pasive way of deletion, that consists in change the active user attribute to False.
    """
    import asyncio
    
    # Create User
    service = UserService()
    create_dto = UserCreateDTO(username="charlyperezk", password="Charly12345", email="carlosperezkuper@gmail.com")
    user_1 = asyncio.run(create_user(service, create_dto))

    # Update User
    update_dto = UserUpdateDTO(username="charlyperezk", email="carlosperezkuper@portus.com")    
    updated_user = asyncio.run(update_user(service, user_1.id, create_dto))

    # Delete User
    _delete_user = asyncio.run(delete_user(service, user_1.id))
    assert _delete_user, "Error deleting user"

    # List all users
    users = asyncio.run(list_all_users(service)) # Must be empty

    # Get by id
    # users = asyncio.run(get_user(service, user_1.id)) # Raise a ValueError if not exists
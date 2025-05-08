import pytest, asyncio
from example.user.service.user_service import UserService
from example.user.dtos.user_dtos import UserCreateDTO, UserUpdateDTO
from portus.common.exceptions import ValidationError

@pytest.fixture
def user_service():
    return UserService()

@pytest.mark.asyncio
async def test_full_user_lifecycle(user_service):
    # 1) Create
    create_dto = UserCreateDTO(
        username="charlyperezk",
        password="Charly12345",
        email="carlosperezkuper@gmail.com",
        country_id=1
    )
    user = await user_service.create(create_dto)
    assert user.id is not None

    # 2) Update
    update_dto = UserUpdateDTO(
        username="charlyp",
        email="carlosperezkuper@portus.com"
    )
    updated = await user_service.update(user.id, update_dto)
    assert updated.username == "charlyp"
    assert updated.email.endswith("@portus.com")

    # 3) Delete (soft delete)
    deleted = await user_service.delete(user.id)
    assert deleted is True

    # 4) List: Must return an empty list.
    users = await user_service.list_all()
    assert users == []

    # 5) Get non-existent should raise
    with pytest.raises(ValidationError):
        await user_service.get("non-existent-id")
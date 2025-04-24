import pytest
from example.user.service.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()
import pytest

from src.application.use_cases.user_service import UserService
from src.domain.entities.user import User
from src.infrastructure.adapters.memory_user_repository import InMemoryUserRepository


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


@pytest.mark.asyncio
async def test_create_user(user_service):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_service.create_user(user)
    assert created_user.id is not None
    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"


@pytest.mark.asyncio
async def test_get_user(user_service):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_service.create_user(user)

    retrieved_user = await user_service.get_user(created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.name == "John Doe"


@pytest.mark.asyncio
async def test_update_user(user_service):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_service.create_user(user)

    updated_data = User(
        id=created_user.id, name="John Updated", email="john.updated@example.com"
    )
    updated_user = await user_service.update_user(updated_data)

    assert updated_user is not None
    assert updated_user.name == "John Updated"
    assert updated_user.email == "john.updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(user_service):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_service.create_user(user)

    deleted = await user_service.delete_user(created_user.id)
    assert deleted is True

    retrieved_user = await user_service.get_user(created_user.id)
    assert retrieved_user is None

import pytest

from src.adapters.repositories.user_repository import UserRepository
from src.domain.entities.user import User


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.mark.asyncio
async def test_create_user(user_repository):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_repository.create(user)
    assert created_user.id is not None
    assert created_user.name == "John Doe"
    assert created_user.email == "john@example.com"


@pytest.mark.asyncio
async def test_get_user(user_repository):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_repository.create(user)

    retrieved_user = await user_repository.get_by_id(created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.name == "John Doe"


@pytest.mark.asyncio
async def test_update_user(user_repository):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_repository.create(user)

    updated_data = User(
        id=created_user.id, name="John Updated", email="john.updated@example.com"
    )
    updated_user = await user_repository.update(updated_data)

    assert updated_user is not None
    assert updated_user.name == "John Updated"
    assert updated_user.email == "john.updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(user_repository):
    user = User(name="John Doe", email="john@example.com")
    created_user = await user_repository.create(user)

    deleted = await user_repository.delete(created_user.id)
    assert deleted is True

    retrieved_user = await user_repository.get_by_id(created_user.id)
    assert retrieved_user is None

from typing import List, Optional

from src.application.ports.user_repository import UserRepository
from src.domain.entities.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()

    async def create_user(self, user: User) -> User:
        return await self.user_repository.create(user)

    async def update_user(self, user: User) -> Optional[User]:
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

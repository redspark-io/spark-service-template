from typing import Dict, List, Optional

from src.domain.entities.user import User
from src.domain.ports.user_port import UserPort
from src.domain.schemas.user import UserSchema


class UserRepository(UserPort):
    def __init__(self):
        self.users: Dict[str, User] = {}

    async def get_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    async def get_all(self) -> List[User]:
        return list(self.users.values())

    async def create(self, user: UserSchema) -> User:
        if user.id is None:
            user.id = str(len(self.users) + 1)
        self.users[user.id] = user
        return user

    async def update(self, user: UserSchema) -> Optional[User]:
        if user.id in self.users:
            self.users[user.id] = user
            return user
        return None

    async def delete(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

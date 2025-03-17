from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.user import User


class UserPort(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

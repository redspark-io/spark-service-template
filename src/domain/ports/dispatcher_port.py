from abc import ABC, abstractmethod
from typing import Optional


class DispatcherPort(ABC):
    @abstractmethod
    async def dispatch(self, *args) -> Optional[dict]:
        pass

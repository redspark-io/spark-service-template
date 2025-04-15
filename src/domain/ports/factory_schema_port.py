from abc import ABC, abstractmethod
from typing import Optional


class FactorySchemaPort(ABC):
    @abstractmethod
    async def create(self, config: dict) -> Optional[dict]:
        pass

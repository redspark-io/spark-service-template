from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.application import Application


class ApplicationPort(ABC):
    @abstractmethod
    async def create(self, application: Application) -> Optional[Application]:
        pass

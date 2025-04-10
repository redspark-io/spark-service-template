from abc import ABC, abstractmethod
from typing import Optional

from src.domain.schemas.application_schema import ApplicationSchema


class ApplicationPort(ABC):
    @abstractmethod
    async def create(
        self, application: ApplicationSchema
    ) -> Optional[ApplicationSchema]:
        pass

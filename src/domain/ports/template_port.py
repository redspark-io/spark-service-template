from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.models.template import Template


class TemplatePort(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: UUID) -> Optional[Template]:
        pass

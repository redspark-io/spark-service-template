from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.template import Template


class TemplatePort(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: str) -> Optional[Template]:
        pass

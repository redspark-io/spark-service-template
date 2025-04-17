from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.adapters.persistence.entities.template import Template

class TemplatePort(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: UUID) -> Optional[Template]:
        pass

    @abstractmethod
    async def get_all_templates(self) -> list[Template]:
        pass

    @abstractmethod
    async def create_template(self, template: Template) -> Template:
        pass

    @abstractmethod
    async def delete_template(self, template: Template) -> Template:
        pass

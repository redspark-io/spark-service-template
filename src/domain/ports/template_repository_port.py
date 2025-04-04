from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.template import Template


class TemplateRepositoryPort(ABC):

    def __init__(self, db):
        self.db = db

    @abstractmethod
    async def get_by_id(self, template_id: str) -> Optional[Template]:
        pass

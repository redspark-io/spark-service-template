from uuid import UUID

from src.domain.exceptions.template_exceptions import TemplateNotFoundException
from src.domain.ports.template_port import TemplatePort


class TemplateGetConfigService:
    def __init__(
        self,
        template_repository: TemplatePort,
    ):
        self.template_repository = template_repository

    async def handler(self, template_id: UUID):
        print(template_id)
        template = await self.template_repository.get_by_id(template_id)
        if not template:
            TemplateNotFoundException()
        return template.config  # type: ignore

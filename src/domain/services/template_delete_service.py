from uuid import UUID
from src.domain.exceptions.template_exceptions import TemplateNotFoundException
from src.domain.ports.template_port import TemplatePort


class TemplateDeleteService:
    def __init__(
        self,
        template_repository: TemplatePort,
    ):
        self.template_repository = template_repository

    async def handler(self, template_id: UUID):
        template = await self.template_repository.get_by_id(template_id)
        if not template:
            TemplateNotFoundException()
        return await self.template_repository.delete(template)

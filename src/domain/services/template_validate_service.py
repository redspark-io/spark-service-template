from src.domain.exceptions.template_exceptions import TemplateNotFoundException
from src.domain.ports.template_port import TemplatePort


class TemplateRunService:
    def __init__(self, template_port: TemplatePort):
        self.template_port = template_port

    async def handler(self, template_id: str):
        template = await self.template_port.get_by_id(template_id)
        if not template:
            raise TemplateNotFoundException()

        return template

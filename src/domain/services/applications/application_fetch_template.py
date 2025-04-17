import json

from jinja2 import Template

from src.domain.models.application import Application
from src.domain.ports.application_port import ApplicationPort


class FetchTemplateService:
    def __init__(self, application_port: ApplicationPort):
        self.application_port = application_port

    async def _parse_inputs(self, inputs: dict, parameters: dict):
        jinja_template = Template(json.dumps(inputs))
        render_jinja = jinja_template.render({"parameters": parameters})
        return json.loads(render_jinja)

    async def handler(self, step_inputs: dict, parameters: dict):
        inputs = await self._parse_inputs(step_inputs, parameters)
        return await self.application_port.create(Application(**inputs))

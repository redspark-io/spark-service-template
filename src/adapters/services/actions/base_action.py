import json

from jinja2 import Template


class BaseAction:
    async def _parse_inputs(self, inputs: dict, parameters: dict):
        jinja_template = Template(json.dumps(inputs))
        render_jinja = jinja_template.render({"parameters": parameters})
        return json.loads(render_jinja)

    async def handler(self, step_inputs: dict, parameters: dict):
        pass

from src.domain.exceptions.template_exceptions import TemplateNotFoundException
from src.domain.ports.dispatcher_port import DispatcherPort
from src.domain.ports.parser_port import ParserPort
from src.domain.ports.template_port import TemplatePort


class TemplateRunService:
    def __init__(
        self,
        template_port: TemplatePort,
        parser_port: ParserPort,
        dispatcher_port: DispatcherPort,
    ):
        self.template_port = template_port
        self.parser_port = parser_port
        self.dispatcher_port = dispatcher_port

    async def handler(self, template_id: str, parameters: dict, token):
        template = await self.template_port.get_by_id(template_id)
        if not template:
            raise TemplateNotFoundException()

        config = await self.parser_port.parser(template.config)
        if not config:
            raise Exception("Invalid config")

        required_fields = []
        for parameter in config["spec"]["parameters"]:
            if parameter["required"]:
                required_fields.extend(parameter["required"])

        missing_fields = []
        for required_field in required_fields:
            if required_field not in parameters or not parameters[required_field]:
                missing_fields.append(required_field)

        if missing_fields:
            raise Exception(f"Missing required field(s): {', '.join(missing_fields)}")

        await self.dispatcher_port.dispatch(config["spec"]["steps"], parameters, token)

        return template

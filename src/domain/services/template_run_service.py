from uuid import UUID

from src.domain.exceptions.template_exceptions import TemplateNotFoundException
from src.domain.ports.dispatcher_port import DispatcherPort
from src.domain.ports.factory_schema_port import FactorySchemaPort
from src.domain.ports.template_port import TemplatePort


class TemplateRunService:
    def __init__(
        self,
        template_port: TemplatePort,
        factory_schema_port: FactorySchemaPort,
        dispatcher_port: DispatcherPort,
        token: str,
    ):
        self.template_port = template_port
        self.factory_schema_port = factory_schema_port
        self.dispatcher_port = dispatcher_port
        self.token = token

    async def handler(self, template_id: UUID, parameters: dict):
        template = await self.template_port.get_by_id(template_id)
        if not template:
            raise TemplateNotFoundException()

        config = await self.factory_schema_port.create(template.config)
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

        await self.dispatcher_port.dispatch(config["spec"]["steps"], parameters)

        return template

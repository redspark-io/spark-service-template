from fastapi import Depends

from src.adapters.clients.spark_service_hub_client import SparkServiceHubClient
from src.adapters.services.actions.base_action import BaseAction
from src.domain.ports.application_port import ApplicationPort
from src.domain.schemas.application_schema import ApplicationSchema
from src.utils.auth import get_current_token


class ApplicationRegisterAction(BaseAction):
    def __init__(self, application_port: ApplicationPort):
        self.application_port = application_port

    async def handler(self, step_inputs: dict, parameters: dict):
        inputs = await self._parse_inputs(step_inputs, parameters)
        return await self.application_port.create(ApplicationSchema(**inputs))


def get_application_register_action(
    token: str = Depends(get_current_token),
) -> ApplicationRegisterAction:
    return ApplicationRegisterAction(SparkServiceHubClient(token))

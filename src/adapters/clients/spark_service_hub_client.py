import aiohttp

from src.domain.ports.application_port import ApplicationPort
from src.domain.schemas.application_schema import ApplicationSchema

SERVICE_HUB_URL = "http://192.168.64.1:81/api"


class SparkServiceHubClient(ApplicationPort):
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    async def create(self, application: ApplicationSchema):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                f"{SERVICE_HUB_URL}/v1/applications", json=application.dict()
            ) as response:
                response = await response.json()
                application_schema = ApplicationSchema(**response)
                return application_schema

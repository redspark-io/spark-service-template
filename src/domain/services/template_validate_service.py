from typing import Optional

import yaml
from fastapi import UploadFile

from src.domain.exceptions.template_exceptions import TemplateInvalidFileTypeException
from src.domain.ports.factory_schema_port import FactorySchemaPort


class TemplateValidateService:
    def __init__(
        self,
        factory_schema_port: FactorySchemaPort,
    ):
        self.factory_schema_port = factory_schema_port

    async def handler(
        self, content_type: Optional[str] = None, file_content: Optional[bytes] = None
    ):
        if not content_type or not file_content:
            raise TemplateInvalidFileTypeException

        if content_type != "text/yaml" and content_type != "text/yml" and content_type != "application/yaml":
            raise TemplateInvalidFileTypeException

        parsed_file = yaml.safe_load(file_content)
        return await self.factory_schema_port.create(parsed_file)

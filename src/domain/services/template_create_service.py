from fastapi import HTTPException, status, UploadFile
from pydantic import ValidationError
import yaml

from src.adapters.api.schemas.template_schema import TemplateSchema
from src.adapters.persistence.entities.template import Template
from src.domain.ports.template_port import TemplatePort
from src.domain.services.template_validate_service import TemplateValidateService


class TemplateCreateService:
    def __init__(
        self,
        template_validate_service: TemplateValidateService,
        template_repository: TemplatePort,
    ):
        self.template_validate_service = template_validate_service
        self.template_repository = template_repository

    async def create_template(self, template: dict, file: UploadFile) -> Template:
        try:
            template_data = yaml.safe_load(template)
            template_schema = TemplateSchema(**template_data)

            template_model = Template(**template_schema.model_dump())
            template_model.config = await self.template_validate_service.handler(
                file.content_type, file.file.read()
            )

            created_template = await self.template_repository.create_template(
                template_model
            )
            return created_template
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]
            )
        finally:
            file.file.close()

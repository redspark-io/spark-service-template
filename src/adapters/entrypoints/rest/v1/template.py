from pydantic import ValidationError
import yaml

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.adapters.repositories.template_repository import TemplateRepository

from src.configs.database import get_db
from src.domain.exceptions.template_exceptions import TemplateInvalidFileTypeException
from src.utils.template_schema_factory import create_template_schema

router = APIRouter()

def get_template_repository(db: AsyncSession = Depends(get_db)) -> TemplateRepository:
    return TemplateRepository(db)


@router.get("/templates/validate")
async def template_validate(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    API GET to Validate template
    """

    try:
        if file.content_type == "text/yaml" or file.content_type == "text/yml":
            parsed_file = yaml.safe_load(file.file.read())
            create_template_schema(parsed_file)
        else:
            raise TemplateInvalidFileTypeException
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    finally:
        file.file.close()

    return {"message": f"Successfully parserd {file.filename}"}


@router.post("/templates/{template_id}/run")
async def template_run(template_id: str, form: dict, template_repository: TemplateRepository = Depends(get_template_repository)):
    """
    API POST to Run template
    """

    template = await template_repository.get_by_id(template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

    config: dict = template.config # type: ignore

    template_schema = create_template_schema(config)
    required_fields = []
    for parameter in template_schema.spec.parameters:
        if parameter.required:
            required_fields.extend(parameter.required)

    missing_fields = []
    for required_field in required_fields:
        if required_field not in form or not form[required_field]:
            missing_fields.append(required_field)

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field(s): {', '.join(missing_fields)}",
        )

    for step in template_schema.spec.steps:
        print(step.id)

    return {"message": f"Successfully run template {template_id}"}

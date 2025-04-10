from uuid import UUID

import yaml
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.entrypoints.tasks.template_tasks import step_runner_task
from src.adapters.repositories.template_repository import (
    TemplateRepository,
    get_template_repository,
)
from src.configs.database import get_db
from src.domain.exceptions.template_exceptions import TemplateInvalidFileTypeException
from src.domain.schemas.template_schema import TemplateSchema
from src.domain.schemas.user_schema import UserSchema
from src.utils.auth import get_current_token, get_current_user
from src.utils.template_schema_factory import create_template_schema

router = APIRouter()


@router.get("/api/v1/templates/{template_id}", response_model=TemplateSchema)
async def get_template(
    template_id: UUID,
    template_repository: TemplateRepository = Depends(get_template_repository),
    db: AsyncSession = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    """
    API GET to getting data from template
    """

    template = await template_repository.get_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found"
        )

    return template


@router.get("/api/v1/templates/{template_id}/config")
async def get_template_config(
    template_id: UUID,
    template_repository: TemplateRepository = Depends(get_template_repository),
    db: AsyncSession = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    """
    API GET to getting config from template
    """

    template = await template_repository.get_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found"
        )

    template_schema = create_template_schema(template.config)  # type: ignore

    return template_schema


@router.post("/api/v1/templates/validate")
async def template_validate(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: UserSchema = Depends(get_current_user),
):
    """
    API post to validate template
    """

    try:
        if file.content_type == "text/yaml" or file.content_type == "text/yml":
            parsed_file = yaml.safe_load(file.file.read())
            create_template_schema(parsed_file)
        else:
            raise TemplateInvalidFileTypeException
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    finally:
        file.file.close()

    return {"message": f"Successfully parserd {file.filename}"}


@router.post("/api/v1/templates/{template_id}/run")
async def template_run(
    template_id: UUID,
    parameters: dict,
    template_repository: TemplateRepository = Depends(get_template_repository),
    token: str = Depends(get_current_token),
    user: UserSchema = Depends(get_current_user),
):
    """
    API POST to run template
    """

    template = await template_repository.get_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found"
        )

    config: dict = template.config  # type: ignore

    template_schema = create_template_schema(config)
    required_fields = []
    for parameter in template_schema.spec.parameters:
        if parameter.required:
            required_fields.extend(parameter.required)

    missing_fields = []
    for required_field in required_fields:
        if required_field not in parameters or not parameters[required_field]:
            missing_fields.append(required_field)

    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field(s): {', '.join(missing_fields)}",
        )

    steps = [step.model_dump() for step in template_schema.spec.steps]

    step_runner_task.delay(steps, parameters, token)

    return {"message": f"Successfully run template {template_id}"}

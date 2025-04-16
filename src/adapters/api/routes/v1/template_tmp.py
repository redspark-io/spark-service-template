from typing import Annotated
from uuid import UUID
import os  # Import necessário para manipular extensões de arquivos

import yaml
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Form
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.schemas.template.template_factory_schema import TemplateSchemaFactory, get_template_factory
from src.adapters.api.schemas.template_schema import TemplateResponseSchema, TemplateSchema
from src.adapters.api.schemas.user_schema import UserSchema
from src.adapters.persistence.repositories.template_repository import (
    TemplateRepository,
    get_template_repository,
)
from src.adapters.tasks.template_tasks import step_runner_task
from src.domain.exceptions.template_exceptions import TemplateInvalidFileTypeException
from src.adapters.persistence.entities.template import Template
from src.domain.services.template_create_service import TemplateCreateService
from src.domain.services.template_run_service import TemplateRunService
from src.domain.services.template_validate_service import TemplateValidateService
from src.infrastructure.database import get_db
from src.utils.auth import get_current_token, get_current_user

router = APIRouter()

def get_template_validate_service(
    factory_schema=Depends(get_template_factory),
):
    return TemplateValidateService(factory_schema)

def get_template_create_service(
    template_validate_service=Depends(get_template_validate_service),
    template_repository=Depends(get_template_repository),
):
    return TemplateCreateService(template_validate_service, template_repository)


@router.get("/api/v1/templates", response_model=list[TemplateResponseSchema])
async def get_templates(
    template_repository: TemplateRepository = Depends(get_template_repository),
    # user: UserSchema = Depends(get_current_user)
):
    """
    API GET to getting templates
    """
    return await template_repository.get_all_templates()


@router.post("/api/v1/templates", response_model=TemplateResponseSchema)
async def create_template(
    template:  Annotated[str, Form()],
    file: UploadFile = File(...),
    template_create_service: TemplateCreateService = Depends(
        get_template_create_service
    ),
):
    """
    API POST to creating a template
    """

    return await template_create_service.create_template(template, file)

@router.delete("/api/v1/templates/{template_id}")
async def delete_template(
    template_id: UUID,
    template_repository: TemplateRepository = Depends(get_template_repository),
    # user: UserSchema = Depends(get_current_user)
):
    """
    API DELETE to deleting a template
    """
    template = await template_repository.get_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Template not found"
        )

    await template_repository.delete_template(template)
    return {"message": "Template deleted successfully"}

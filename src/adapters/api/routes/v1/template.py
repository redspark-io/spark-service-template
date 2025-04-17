from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError

from src.adapters.api.schemas.template.template_factory_schema import (
    get_template_factory,
)
from src.adapters.api.schemas.template_schema import TemplateSchema
from src.adapters.api.schemas.user_schema import UserSchema
from src.adapters.persistence.repositories.template_repository import (
    get_template_repository,
)
from src.adapters.tasks.dispatcher_tasks import get_template_step_runner_dispatcher
from src.domain.services.template_get_config_service import TemplateGetConfigService
from src.domain.services.template_get_service import TemplateGetService
from src.domain.services.template_run_service import TemplateRunService
from src.domain.services.template_validate_service import TemplateValidateService
from src.utils.auth import get_current_token, get_current_user

router = APIRouter()


def get_template_run_service(
    template_repository=Depends(get_template_repository),
    template_parser=Depends(get_template_factory),
    template_step_runner_dispatcher=Depends(get_template_step_runner_dispatcher),
    token: str = Depends(get_current_token),
):
    return TemplateRunService(
        template_repository, template_parser, template_step_runner_dispatcher, token
    )


def get_template_validate_service(
    factory_schema=Depends(get_template_factory),
):
    return TemplateValidateService(factory_schema)


def get_template_get_config_service(
    template_repository=Depends(get_template_repository),
):
    return TemplateGetConfigService(template_repository)


def get_template_get_service(
    template_repository=Depends(get_template_repository),
):
    return TemplateGetService(template_repository)


@router.get("/api/v1/templates/{template_id}", response_model=TemplateSchema)
async def get_template(
    template_id: UUID,
    template_get_service: TemplateGetService = Depends(get_template_get_service),
    user: UserSchema = Depends(get_current_user),
):
    """
    API GET to getting data from template
    """
    try:
        return await template_get_service.handler(template_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])


@router.get("/api/v1/templates/{template_id}/config")
async def get_template_config(
    template_id: UUID,
    template_get_config_service: TemplateGetConfigService = Depends(
        get_template_get_config_service
    ),
    user: UserSchema = Depends(get_current_user),
):
    """
    API GET to getting config from template
    """
    try:
        return await template_get_config_service.handler(template_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])


@router.post("/api/v1/templates/validate")
async def template_validate(
    file: UploadFile = File(...),
    template_validate_service: TemplateValidateService = Depends(
        get_template_validate_service
    ),
    user: UserSchema = Depends(get_current_user),
):
    """
    API post to validate template
    """

    try:
        await template_validate_service.handler(file.content_type, file.file.read())
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
    template_run_service: TemplateRunService = Depends(get_template_run_service),
    user: UserSchema = Depends(get_current_user),
):
    """
    API POST to run template
    """

    try:
        await template_run_service.handler(template_id, parameters)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])

    return {"message": f"Successfully run template {template_id}"}

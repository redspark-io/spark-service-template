import asyncio
import logging

from src.adapters.api.schemas.template.v1beta1.enums.action import ActionEnum
from src.adapters.clients.spark_service_hub_client import SparkServiceHubClient
from src.domain.services.applications.application_fetch_template import FetchTemplateService
from src.domain.services.applications.application_register_service import (
    ApplicationRegisterService,
)
from src.infrastructure.celery import CustomBaseTask, celery_app

logger = logging.getLogger("uvicorn")


@celery_app.task(
    base=CustomBaseTask,
    name="step_runner_task",
)
def step_runner_task(steps, parameters, token):
    logger.info("Task starting...")
    outputs = {}
    for step in steps:
        if step["action"] == ActionEnum.fetch_template:
            application_register_service = FetchTemplateService(
                SparkServiceHubClient(token)
            )
            outputs[step["id"]] = asyncio.run(
                application_register_service.handler(step["input"], parameters)
            )
        elif step["action"] == ActionEnum.application_register:
            application_register_service = ApplicationRegisterService(
                SparkServiceHubClient(token)
            )
            outputs[step["id"]] = asyncio.run(
                application_register_service.handler(step["input"], parameters)
            )
    logger.info("Task runing with success")

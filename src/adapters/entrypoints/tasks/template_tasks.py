import asyncio
import logging

from src.adapters.clients.spark_service_hub_client import SparkServiceHubClient
from src.adapters.services.actions.application_register_action import (
    ApplicationRegisterAction,
)
from src.configs.celery import CustomBaseTask, celery_app
from src.domain.schemas.template.v1beta1.enums.action import ActionEnum

logger = logging.getLogger("uvicorn")


@celery_app.task(
    base=CustomBaseTask,
    name="step_runner_task",
)
def step_runner_task(steps, parameters, token):
    logger.info("Task starting...")
    outputs = {}
    for step in steps:
        if step["action"] == ActionEnum.application_register:
            application_register_action = ApplicationRegisterAction(
                SparkServiceHubClient(token)
            )
            outputs[step["id"]] = asyncio.run(
                application_register_action.handler(step["input"], parameters)
            )
    logger.info("Task runing with success")

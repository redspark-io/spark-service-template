import logging

from src.infrastructure.celery import CustomBaseTask, celery_app

logger = logging.getLogger(__name__)


@celery_app.task(
    base=CustomBaseTask,
    name="sample_task",
)
def sample_task():
    print("Task runing with success")

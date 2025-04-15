import logging

from celery import Celery, Task

from src.infrastructure.configs import settings

# from celery.schedules import crontab


logger = logging.getLogger(__name__)


celery_app = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],
)

celery_app.autodiscover_tasks(["src.adapters.tasks"])

# celery_app.conf.beat_schedule = {
#     "add-every-minute-sample-task": {
#         "task": "sample_task",
#         "schedule": crontab(),
#     },
# }


class CustomBaseTask(Task):
    ignore_result = True
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 5

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.warning(
            "%s[%s] NOTIFICATION FOR FAILURE DETECTED FOR TASK", self.name, task_id
        )

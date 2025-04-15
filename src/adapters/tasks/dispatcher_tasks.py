from fastapi import Depends

from src.adapters.tasks.template_tasks import step_runner_task
from src.domain.ports.dispatcher_port import DispatcherPort
from src.utils.auth import get_current_token


class TemplateStepRunnerDispatcher(DispatcherPort):
    def __init__(self, token: str):
        self.token = token

    async def dispatch(self, steps, parameters):
        step_runner_task.delay(steps, parameters, self.token)


def get_template_step_runner_dispatcher(token=Depends(get_current_token)):
    return TemplateStepRunnerDispatcher(token)

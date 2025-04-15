from src.adapters.tasks.template_tasks import step_runner_task
from src.domain.ports.dispatcher_port import DispatcherPort


class TemplateStepDispatcher(DispatcherPort):
    async def dispatch(self, steps, parameters, token):
        step_runner_task.delay(steps, parameters, token)


def get_template_step_dispatcher():
    return TemplateStepDispatcher()

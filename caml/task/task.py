from abc import ABC, abstractmethod
from typing import Any, Dict

from clearml import Task as _Task

EXECUTION_PARAMS = 'Execution'


class Task(ABC):
    _requirements = [
        ('clearml', ''),
        ('yacs', ''),
    ]
    _task_init: Dict[str, Any] = {
        'output_uri': True,
        'auto_connect_arg_parser': False,
    }

    def __init__(
        self,
        project_name: str,
        task_name: str,
        task_init: Dict[str, Any] = None,
        execution: Dict[str, Any] = None,
        requirement_file: str = None,
        remote: bool = False,
        queue_name: str = 'default',
    ):
        super(Task, self).__init__()
        self.project_name = project_name
        self.task_name = task_name
        self.task_init = task_init if task_init else {}
        self.execution = execution if execution else {}
        self.requirement_file = requirement_file
        self.remote = remote
        self.queue_name = queue_name

    @property
    def _task(self):
        return _Task.current_task()

    def run(self) -> None:
        for requirement in Task._requirements:
            _Task.add_requirements(*requirement)

        if self.requirement_file:
            _Task.add_requirements(self.requirement_file)

        _Task.init(
            project_name=self.project_name,
            task_name=self.task_name,
            **{**Task._task_init, **self.task_init},
        )

        if self.execution:
            self._task.connect(
                self.execution,
                name=EXECUTION_PARAMS,
            )

        if self.remote:
            self._task.execute_remotely(self.queue_name)

        self.execute(**self.execution)

    @abstractmethod
    def execute(self, **kwargs: Any) -> None:
        pass

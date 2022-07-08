from abc import ABC, abstractmethod
from typing import Any, Dict, List

from clearml import Task as _Task

EXECUTION_PARAMS = 'Execution'


class Task(ABC):
    _requirements = [
        ('clearml', ''),
        ('yacs', ''),
        ('git+https://github.com/tronglh241/caml.git', '')
    ]
    _task_init: Dict[str, Any] = {
        'output_uri': True,
    }

    def __init__(
        self,
        project_name: str,
        task_name: str,
        task_init: Dict[str, Any] = None,
        execution: Dict[str, Any] = None,
        requirement_file: str = None,
        ignored_requirements: List[str] = None,
        remote: bool = False,
        queue_name: str = 'default',
    ):
        super(Task, self).__init__()
        self.project_name = project_name
        self.task_name = task_name
        self.task_init = task_init if task_init else {}
        self.execution = execution if execution else {}
        self.requirement_file = requirement_file
        self.ignored_requirements = ignored_requirements
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

        if self.ignored_requirements:
            for ignored_requirement in self.ignored_requirements:
                _Task.ignore_requirements(ignored_requirement)

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

        self._task.output_uri = self._task_init['output_uri']
        self.execute(**self.execution)

    @abstractmethod
    def execute(self, **kwargs: Any) -> None:
        pass

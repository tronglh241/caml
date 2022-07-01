from typing import Any, Dict

from clearml import Dataset as _Dataset
from clearml import TaskTypes

from caml.config import Config
from caml.task.data.strategy.strategy import Strategy
from caml.task.task import Task


class DataQueryTask(Task):
    def __init__(
        self,
        project_name: str,
        task_name: str,
        task_init: Dict[str, Any] = None,
        execution: Dict[str, Any] = None,
        requirement_file: str = None,
        remote: bool = False,
    ):
        task_init = task_init if task_init else {}
        task_init['task_type'] = TaskTypes.data_processing
        super(DataQueryTask, self).__init__(
            project_name=project_name,
            task_name=task_name,
            task_init=task_init,
            execution=execution,
            requirement_file=requirement_file,
            remote=remote,
        )

    def execute(
        self,
        dataset_name: str,
        dataset_project: str,
        strategy: str,
        data_source_conf: Dict[str, Any],
        model_conf: Dict[str, Any] = None,
        n_samples: int = None,
        **strategy_kwargs: Any,
    ) -> None:
        data_source = Config(data_source_conf).eval()
        model = Config(model_conf).eval() if model_conf else None

        _strategy = Strategy.get(strategy, **strategy_kwargs)
        samples = data_source.samples()
        samples = _strategy.query(samples, n_samples, model)
        data_path = data_source.create_dataset(samples)
        dataset = _Dataset.create(
            dataset_name=dataset_name,
            dataset_project=dataset_project,
            use_current_task=True,
        )
        dataset.add_files(path=data_path)
        dataset.upload()
        dataset.finalize()

from typing import Any, Dict

from clearml import Dataset as _Dataset
from clearml import TaskTypes

from caml.config import Config
from caml.strategy.strategy import Strategy
from caml.task.task import Task


class DataQueryTask(Task):
    def __init__(
        self,
        **kwargs: Any,
    ):
        task_init = kwargs.pop('task_init', {})
        task_init['task_type'] = TaskTypes.data_processing
        super(DataQueryTask, self).__init__(
            task_init=task_init,
            **kwargs,
        )

    def execute(
        self,
        dataset_name: str,
        strategy: str,
        data_source_conf: Dict[str, Any],
        model_conf: Dict[str, Any] = None,
        n_samples: int = None,
        **strategy_kwargs: Any,
    ) -> None:
        data_source = Config(data_source_conf).eval()
        model = Config(model_conf).eval() if model_conf else None

        _strategy = Strategy.get(strategy, **strategy_kwargs)

        samples, targets = data_source.samples()
        indices = _strategy.query(samples, n_samples, model)
        samples = [samples[i] for i in indices]

        if targets:
            targets = [targets[i] for i in indices]

        data_path = data_source.create_dataset(samples, targets)
        dataset = _Dataset.create(
            dataset_name=dataset_name,
            dataset_project=self.project_name,
            use_current_task=True,
        )
        dataset.add_files(path=data_path)
        dataset.upload()
        dataset.finalize()

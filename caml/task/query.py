from typing import Any, Dict

from clearml import Dataset as _Dataset
from clearml import TaskTypes

from caml.data_source import DataSource
from caml.model import EvalModel
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
        strategy: str,
        data_source: DataSource,
        model: EvalModel = None,
        strategy_kwargs: Dict[str, Any] = None,
        n_samples: int = None,
    ) -> None:
        _strategy_kwargs = {} if strategy_kwargs is None else strategy_kwargs
        _strategy = Strategy.get(strategy, **_strategy_kwargs)

        samples, targets = data_source.samples()
        indices = _strategy.query(samples, n_samples, model)
        samples = [samples[i] for i in indices]

        if targets:
            targets = [targets[i] for i in indices]

        data_path = data_source.create_dataset(samples, targets)
        dataset = _Dataset.create(
            dataset_project=self.project_name,
            dataset_name=self.task_name,
        )
        dataset.add_files(path=data_path)
        dataset.upload()
        dataset.finalize()

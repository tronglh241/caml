from abc import ABC, abstractmethod
from typing import Any, Dict

from caml.config import Config
from caml.dataset import Dataset
from caml.model import EvalModel, Model, TrainModel
from caml.task.task import Task


class DLTask(Task, ABC):
    def execute(
        self,
        model_conf: Dict[str, Any],
        dataset_conf: Dict[str, Any],
    ) -> None:
        model = Config(model_conf).eval()
        dataset = Config(dataset_conf).eval()
        self.process(model, dataset)

    @abstractmethod
    def process(
        self,
        model: Model,
        dataset: Dataset,
    ) -> None:
        pass


class TrainTask(DLTask):
    def process(
        self,
        model: TrainModel,
        dataset: Dataset,
    ) -> None:
        dataset.load()
        model.load()
        X = dataset.X()
        y = dataset.y()
        model.fit(X, y)
        best_model = model.best_model()

        if best_model:
            self.upload_model(best_model)

    def upload_model(
        self,
        path: str,
    ) -> None:
        self._task.update_output_model(
            path,
        )


class EvalTask(DLTask):
    def process(
        self,
        model: EvalModel,
        dataset: Dataset,
    ) -> None:
        dataset.load()
        model.load()
        X = dataset.X()
        y = dataset.y()
        pred = model.predict(X)
        score_name, score_value = model.eval(pred, y)
        self.upload_score(score_name, score_value)

    def upload_score(
        self,
        name: str,
        value: float,
    ) -> None:
        self._task.get_logger().report_scalar(
            title=name,
            series='best',
            value=value,
            iteration=1,
        )

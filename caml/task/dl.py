from caml.dataset import Dataset
from caml.model import EvalModel, TrainModel
from caml.task.task import Task


class TrainTask(Task):
    def execute(
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


class EvalTask(Task):
    def execute(
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
            title='Evaluation',
            series=name,
            value=value,
            iteration=1,
        )

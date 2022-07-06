from typing import Optional, Tuple

from caml.model import EvalModel, TrainModel


class UnnamedTrainModel(TrainModel):
    def __init__(self, path: str = None, id_: str = None):
        super(UnnamedTrainModel, self).__init__(path=path, id_=id_)

    def fit(self, X: list, y: list) -> None:
        pass

    def load_model(self, path: str) -> None:
        pass

    def best_model(self) -> Optional[str]:
        pass


class UnnamedEvalModel(EvalModel):
    def __init__(self):
        pass

    def predict(self, X: list) -> list:
        pass

    def predict_proba(self, X: list) -> list:
        pass

    def eval(self, pred: list, y: list) -> Tuple[str, float]:
        pass

    def load_model(self, path: str) -> None:
        pass

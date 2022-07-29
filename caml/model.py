from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from clearml import Model as _Model


class Model(ABC):
    def __init__(
        self,
        path: str = None,
        id_: str = None,
    ):
        self.path = path
        self.id = id_

    def load(self) -> None:
        if self.id is not None:
            path = _Model(self.id).get_local_copy()
        else:
            path = self.path

        if path:
            self.load_model(path)

    @abstractmethod
    def load_model(
        self,
        path: str,
    ) -> None:
        pass


class TrainModel(Model):
    @abstractmethod
    def fit(
        self,
        X: list,
        y: list,
    ) -> None:
        pass

    @abstractmethod
    def best_model(self) -> Optional[str]:
        pass


class EvalModel(Model):
    @abstractmethod
    def predict(
        self,
        X: list,
    ) -> list:
        pass

    @abstractmethod
    def predict_proba(
        self,
        X: list,
    ) -> list:
        pass

    @abstractmethod
    def eval(
        self,
        pred: list,
        y: list,
    ) -> Tuple[str, float]:
        pass

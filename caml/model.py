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
        if id_ is not None:
            self.path = _Model(id_).get_local_copy()
        else:
            self.path = path

    def load(self) -> None:
        if self.path:
            self.load_model(self.path)

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

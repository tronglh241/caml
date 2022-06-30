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
        elif path is not None:
            self.path = path
        else:
            raise ValueError('Must specify `path` or `id_`.')

    @abstractmethod
    def fit(
        self,
        X: list,
        y: list,
    ) -> None:
        pass

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

    @abstractmethod
    def load_model(self, path: str) -> None:
        pass

    @abstractmethod
    def best_model(self) -> Optional[str]:
        pass

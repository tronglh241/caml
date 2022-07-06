from __future__ import annotations

from abc import ABC, abstractmethod

from clearml import Dataset as _Dataset


class Dataset(ABC):
    def __init__(
        self,
        path: str = None,
        id_: str = None,
    ):
        if id_ is not None:
            self.path = _Dataset.get(id_).get_local_copy()
        elif path is not None:
            self.path = path
        else:
            raise ValueError('Must specify `path` or `id_`.')

    @abstractmethod
    def X(self) -> list:
        pass

    @abstractmethod
    def y(self) -> list:
        pass

    @abstractmethod
    def load_dataset(
        self,
        path: str,
    ) -> None:
        pass

    def load(self) -> None:
        self.load_dataset(self.path)

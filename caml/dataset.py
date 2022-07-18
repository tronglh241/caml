from __future__ import annotations

from abc import ABC, abstractmethod

from clearml import Dataset as _Dataset


class Dataset(ABC):
    def __init__(
        self,
        path: str = None,
        id_: str = None,
    ):
        self.path = path
        self.id = id_

        if (path is None) == (id_ is None):
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
        if self.id is not None:
            path = _Dataset.get(self.id).get_local_copy()
        elif self.path is not None:
            path = self.path

        self.load_dataset(path)

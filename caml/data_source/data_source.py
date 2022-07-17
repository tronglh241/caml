from abc import ABC, abstractmethod
from typing import Tuple


class DataSource(ABC):
    @abstractmethod
    def samples(self) -> Tuple[list, list]:
        pass

    @abstractmethod
    def create_dataset(
        self,
        samples: list,
        targets: list,
    ) -> str:
        pass

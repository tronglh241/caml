from abc import ABC, abstractmethod
from typing import Optional, Tuple


class DataSource(ABC):
    @abstractmethod
    def samples(self) -> Tuple[list, Optional[list]]:
        pass

    @abstractmethod
    def create_dataset(
        self,
        samples: list,
        targets: list = None,
    ) -> str:
        pass

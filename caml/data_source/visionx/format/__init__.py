from abc import ABC, abstractmethod


class Format(ABC):
    def __init__(
        self,
        data_dir: str,
    ):
        super(Format, self).__init__()
        self.data_dir = data_dir

    @abstractmethod
    def samples(self) -> list:
        pass

    @abstractmethod
    @staticmethod
    def merge(samples: list) -> str:
        pass

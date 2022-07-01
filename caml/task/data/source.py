from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def samples(self) -> list:
        pass

    @abstractmethod
    def create_dataset(self) -> str:
        pass

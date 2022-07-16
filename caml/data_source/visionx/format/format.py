from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Type


class Format(ABC):
    FORMATS: Dict[str, Type[Format]] = {}

    def __init__(
        self,
        data_dir: str,
    ):
        super(Format, self).__init__()
        self.data_dir = data_dir

    @abstractmethod
    def samples(self) -> list:
        pass

    @staticmethod
    @abstractmethod
    def merge(samples: list) -> str:
        pass

    @staticmethod
    def get(name: str) -> Type[Format]:
        if name in Format.FORMATS:
            return Format.FORMATS[name]
        else:
            raise ValueError(f'Unsupported name {name}. Please use one of {list(Format.FORMATS)}.')

    @staticmethod
    def choices() -> List[str]:
        return list(Format.FORMATS)


def register_format(name):
    def decorator(format_):
        if name in Format.FORMATS:
            raise ValueError(f'`{name}` is already registered.')

        Format.FORMATS[name] = format_
        return format_

    return decorator

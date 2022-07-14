from __future__ import annotations

from abc import abstractclassmethod, abstractproperty
from typing import Any


class Element:
    @abstractclassmethod
    def parse(cls, obj: Any) -> Element:
        pass

    @abstractproperty
    def json(self) -> Any:
        pass

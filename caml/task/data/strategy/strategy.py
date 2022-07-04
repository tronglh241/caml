from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from caml.model import Model


class Strategy(ABC):
    STRATEGIES: Dict[str, Type[Strategy]] = {}

    @abstractmethod
    def query(
        self,
        pool: list,
        n_samples: int = None,
        model: Model = None,
    ) -> list:
        pass

    @staticmethod
    def get(strategy: str, **kwargs: Any) -> Strategy:
        if strategy in Strategy.STRATEGIES:
            return Strategy.STRATEGIES[strategy](**kwargs)
        else:
            raise ValueError(f'Unsupported strategy {strategy}. Please use one of {Strategy.STRATEGIES}.')


def register_strategy(name):
    def decorator(strategy):
        Strategy.STRATEGIES[name] = strategy
        return strategy

    return decorator

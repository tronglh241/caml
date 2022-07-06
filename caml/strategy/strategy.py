from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

from caml.model import EvalModel


class Strategy(ABC):
    STRATEGIES: Dict[str, Type[Strategy]] = {}

    @abstractmethod
    def query(
        self,
        pool: list,
        n_samples: int = None,
        model: EvalModel = None,
    ) -> List[int]:
        pass

    @staticmethod
    def get(
        strategy: str,
        **kwargs: Any,
    ) -> Strategy:
        if strategy in Strategy.STRATEGIES:
            return Strategy.STRATEGIES[strategy](**kwargs)
        else:
            raise ValueError(f'Unsupported strategy {strategy}. Please use one of {Strategy.STRATEGIES}.')


def register_strategy(name):
    def decorator(strategy):
        if name in Strategy.STRATEGIES:
            raise ValueError(f'`{name}` is already registered.')

        Strategy.STRATEGIES[name] = strategy
        return strategy

    return decorator

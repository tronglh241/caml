import random
from typing import List

from caml.model import EvalModel

from .strategy import Strategy, register_strategy


@register_strategy(name='random')
class Random(Strategy):
    def query(
        self,
        pool: list,
        n_samples: int = None,
        model: EvalModel = None,
    ) -> List[int]:
        _n_samples = len(pool) if n_samples is None else n_samples
        samples = random.sample(population=range(len(pool)), k=_n_samples)
        return samples

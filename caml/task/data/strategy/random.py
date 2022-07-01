import random

from caml.model import Model

from .strategy import Strategy, register_strategy


@register_strategy(name='random')
class Random(Strategy):
    def query(
        self,
        pool: list,
        n_samples: int = None,
        model: Model = None,
    ) -> list:
        _n_samples = len(pool) if n_samples is None else n_samples
        samples = random.sample(population=pool, k=_n_samples)
        return samples

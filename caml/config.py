from __future__ import annotations

import warnings
from importlib import import_module
from typing import Any, Dict

import yaml
from yacs.config import CfgNode

Keyword = CfgNode()
Keyword.NOT_EVAL = CfgNode()
Keyword.NOT_EVAL.MODULE = 'module'
Keyword.NOT_EVAL.NAME = 'name'
Keyword.MODULE = Keyword.NOT_EVAL.MODULE
Keyword.NAME = Keyword.NOT_EVAL.NAME
Keyword.KWARGS = 'kwargs'


def _eval(
    config: Any,
    globals_: Dict[str, Any] = None,
    locals_: Dict[str, Any] = None,
) -> Any:
    if isinstance(config, dict):
        for key, value in config.items():
            if key not in Keyword.NOT_EVAL.values():
                config[key] = _eval(value, globals_, locals_)

        if Keyword.MODULE in config and Keyword.NAME in config:
            module = config.pop(Keyword.MODULE)
            name = config.pop(Keyword.NAME)
            config_kwargs = config.pop(Keyword.KWARGS, {})

            if config:
                warnings.warn(f'Redundant keys {list(config.keys())} in module {module}, name {name}.')

            return eval(name, {}, vars(import_module(module)))(**config_kwargs)

    elif isinstance(config, list):
        config = list(map(lambda ele: _eval(ele, globals_, locals_), config))

    return config


class Config(CfgNode):
    def eval(self) -> Any:
        config = org_config = self.clone()
        config = _eval(config, None, org_config)
        return config

    @staticmethod
    def load(file: str) -> Config:
        with open(file) as f:
            config = Config(yaml.safe_load(f))

        return config

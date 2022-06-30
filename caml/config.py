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
Keyword.EXTRALIBS = 'extralibs'


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

    elif isinstance(config, str):
        config = eval(config, globals_, locals_)

    return config


class Config(CfgNode):
    def eval(self) -> Any:
        config = org_config = self.clone()
        extralibs = CfgNode()

        # Generate extra libs
        for alias, lib_info in config.pop(Keyword.EXTRALIBS, {}).items():
            if isinstance(lib_info, dict):
                module = lib_info[Keyword.MODULE]
                name = lib_info[Keyword.NAME]
                lib = getattr(import_module(module), name)
            else:
                lib = import_module(lib_info)

            extralibs[alias] = lib

        # Eval config
        config = _eval(config, extralibs, org_config)

        if extralibs:
            config[Keyword.EXTRALIBS] = extralibs

        return config

    @staticmethod
    def load(file: str) -> Config:
        with open(file) as f:
            config = Config(yaml.safe_load(f))

        return config

    def state_dict(self) -> str:
        return self.dump(sort_keys=False)

from typing import Any, Dict
from caml import Config, Task, DataSource


class DataQueryTask(Task):
    def execute(
        self,
        strategy: str,
        data_source_conf: Dict[str, Any],
        model_conf: Dict[str, Any],
    ) -> None:
        data_source = Config(data_source_conf).eval()
        model = Config(model_conf).eval()

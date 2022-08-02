from __future__ import annotations

import getpass
import zipfile
from pathlib import Path
from typing import List, Optional, Tuple

from clearml import Task as _Task

from ..data_source import DataSource
from .anno_downloader import ProjectAnnoDownloader, TaskAnnoDownloader
from .format.format import Format
from .token import Token

TOKEN_GROUP_NAME = 'Token'
ACCESS_TOKEN = 'access_token'
EXPIRES_IN = 'expires_in'
REFRESH_EXPIRES_IN = 'refresh_expires_in'
REFRESH_TOKEN = 'refresh_token'
REQUEST_TIME = 'request_time'


class VisionX(DataSource):
    def __init__(
        self,
        format_: str = 'CVAT for images 1.1',
        project_id: int = None,
        task_ids: List[int] = None,
        timeout: int = 120,
    ):
        super(VisionX, self).__init__()
        self.project_id = project_id
        self.task_ids = task_ids
        self.format = format_
        self.timeout = timeout
        self.format_handler = Format.get(format_)

        if format_ not in Format.choices():
            raise ValueError(f'`format_` must be one of {Format.choices()}.')

        if (project_id is None) == (task_ids is None):
            raise ValueError('Either `project_id` or `task_ids` is specified.')

        _token = self.get_token()

        if not _token:
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            self.token = Token.request(username, password)
            self.set_token(self.token)
        else:
            self.token = _token

    def get_token(self) -> Optional[Token]:
        task = _Task.current_task()
        task_params = task.get_parameters_as_dict(cast=True)

        if TOKEN_GROUP_NAME in task_params:
            token_params = task_params[TOKEN_GROUP_NAME]
            return Token(
                access_token=token_params[ACCESS_TOKEN],
                expires_in=token_params[EXPIRES_IN],
                refresh_expires_in=token_params[REFRESH_EXPIRES_IN],
                refresh_token=token_params[REFRESH_TOKEN],
                request_time=token_params[REQUEST_TIME],
            )

        return None

    def set_token(
        self,
        token: Token,
    ) -> None:
        task = _Task.current_task()
        task.set_parameters_as_dict({
            TOKEN_GROUP_NAME: {
                ACCESS_TOKEN: token.access_token,
                EXPIRES_IN: token.expires_in,
                REFRESH_EXPIRES_IN: token.refresh_expires_in,
                REFRESH_TOKEN: token.refresh_token,
                REQUEST_TIME: token.request_time,
            },
        })

    def samples(self) -> Tuple[List[str], list]:
        _samples, targets = [], []

        if self.project_id is not None:
            task_anno_zips = ProjectAnnoDownloader(
                format_=self.format,
                token=self.token,
                timeout=self.timeout,
            )(self.project_id)
        elif self.task_ids is not None:
            task_anno_downloader = TaskAnnoDownloader(
                format_=self.format,
                token=self.token,
                timeout=self.timeout,
            )
            task_anno_zips = [task_anno_downloader(task_id) for task_id in self.task_ids]

        for anno_zip in task_anno_zips:
            anno_dir = Path(anno_zip).with_suffix('')
            anno_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(anno_zip, 'r') as zr:
                zr.extractall(str(anno_dir))

            Path(anno_zip).unlink()

            task_samples = self.format_handler(str(anno_dir)).samples()

            for sample, target in task_samples:
                _samples.append(sample)
                targets.append(target)

        return _samples, targets

    def create_dataset(
        self,
        samples: List[str],
        targets: list,
    ) -> str:
        return self.format_handler.merge(list(zip(samples, targets)))

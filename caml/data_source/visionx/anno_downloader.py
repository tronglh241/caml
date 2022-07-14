import time
from enum import Enum
from __future__ import annotations
from typing import List
import requests
import shutil
from pathlib import Path
import tempfile


BASE_URL = 'https://visionx.smart-data.ml'


class Format(str, Enum):
    CVAT = 'CVAT for images 1.1'
    COCO_MONASH = 'COCO Keypoint for Monash 1.0'

    @classmethod
    def choices(cls) -> List[Format]:
        cs = [c.value for c in cls._member_map_.values()]
        return cs

    def __str__(self) -> str:
        return self.value


class TaskAnnoDownloader:
    def __init__(
        self,
        format_: str,
        token: str,
        timeout: int = 120,
    ):
        super(TaskAnnoDownloader, self).__init__()
        self.format = format_
        self.token = token
        self.timeout = timeout

        if format_ not in Format.choices():
            raise ValueError(f'`format_` must be one of {Format.choices()}.')

    def __call__(
        self,
        task_id: int,
    ) -> str:
        req_start = time.time()

        while time.time() - req_start < self.timeout:
            res = requests.get(
                url=f'{BASE_URL}/api/v1/tasks/{task_id}/dataset',
                params={
                    'format': self.format,
                    'action': 'download',
                },
                headers={
                    'Authorization': f'Bearer {self.token}',
                },
                stream=True,
            )
            res.raise_for_status()

            if res.status_code == 200:
                break
            else:
                time.sleep(1)

        if res.status_code == 200:
            anno_zip = Path(tempfile.gettempdir()).joinpath(str(task_id)).with_suffix('.zip')

            with anno_zip.open(mode='wb') as f:
                shutil.copyfileobj(res.raw, f)

            return str(anno_zip)
        else:
            raise RuntimeError(f'Cannot download annotation for task #{task_id}.')


class ProjectAnnoDownloader:
    def __init__(
        self,
        format_: str,
        token: str,
        timeout: int = 120,
    ):
        super(ProjectAnnoDownloader, self).__init__()
        self.format = format_
        self.token = token
        self.timeout = timeout

        if format_ not in Format.choices():
            raise ValueError(f'`format_` must be one of {Format.choices()}.')

    def __call__(
        self,
        project_id: int,
    ) -> List[str]:
        res = requests.get(
            url=f'{BASE_URL}/api/v1/projects/{project_id}',
            headers={
                'Authorization': f'Bearer {self.token}',
            },
        )
        res.raise_for_status()

        task_anno_downloader = TaskAnnoDownloader(
            format_=self.format,
            token=self.token,
            timeout=self.timeout,
        )
        task_ids = sorted([task['id'] for task in res.json()['tasks']])
        task_anno_zips = [task_anno_downloader(task_id) for task_id in task_ids]

        return task_anno_zips

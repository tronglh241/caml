from __future__ import annotations

import re
import tempfile
import time
from pathlib import Path
from typing import List

import requests
from tqdm import tqdm

from .format.format import Format
from .token import Token

BASE_URL = 'https://visionx.smart-data.ml'


class TaskAnnoDownloader:
    def __init__(
        self,
        format_: str,
        token: Token,
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
                    'Authorization': f'Bearer {self.token.get()}',
                },
                stream=True,
            )
            res.raise_for_status()

            if res.status_code == 200:
                break
            else:
                time.sleep(1)

        if time.time() - req_start > self.timeout:
            raise TimeoutError

        if res.status_code == 200:
            file_size = int(res.headers.get('Content-Length', 0))
            file_names = re.findall('(?<=filename=).*(?=;)', res.headers.get('Content-Disposition', ''))

            if file_names:
                file_name = Path(eval(eval(file_names[0])).decode('utf8'))
            else:
                file_name = Path(str(task_id)).with_suffix('.zip')

            anno_zip = Path(tempfile.gettempdir()).joinpath(file_name)

            if anno_zip.exists() and anno_zip.stat().st_size == file_size:
                print(f'Task #{task_id} is already downloaded.')
            else:
                while not (anno_zip.exists() and anno_zip.stat().st_size == file_size):
                    pbar = tqdm(
                        desc=f'Task #{task_id}',
                        total=file_size,
                        unit='iB',
                        unit_scale=True,
                    )
                    block_size = 1024

                    with anno_zip.open(mode='wb') as f:
                        for data in res.iter_content(block_size):
                            pbar.update(len(data))
                            f.write(data)

                    pbar.close()

            return str(anno_zip)
        else:
            raise RuntimeError(f'Cannot download annotation for task #{task_id}.')


class ProjectAnnoDownloader:
    def __init__(
        self,
        format_: str,
        token: Token,
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
                'Authorization': f'Bearer {self.token.get()}',
            },
        )
        res.raise_for_status()

        task_anno_downloader = TaskAnnoDownloader(
            format_=self.format,
            token=self.token,
            timeout=self.timeout,
        )
        task_ids = sorted([task['id'] for task in res.json()['tasks']])
        task_anno_zips = []

        for task_id in task_ids:
            task_anno_zips.append(task_anno_downloader(task_id))

        return task_anno_zips

from __future__ import annotations

import getpass
import shutil
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from clearml import Task as _Task

from .. import DataSource
from .cvat import Frame, Label
from .anno_downloader import Format, ProjectAnnoDownloader
from .token import Token


class VisionX(DataSource):
    PARAM_NAME = 'Token/VisionX'

    def __init__(
        self,
        project_id: int,
        format_: str = Format.CVAT,
        timeout: int = 120,
    ):
        super(VisionX, self).__init__()
        self.project_id = project_id
        self.format = format_
        self.timeout = timeout

        if format_ not in Format.choices():
            raise ValueError(f'`format_` must be one of {Format.choices()}.')

        task = _Task.current_task()
        token = task.get_parameter(VisionX.PARAM_NAME)

        if not token:
            username = input('Username: ')
            password = getpass.getpass('Password: ')
            token = Token.request(username, password)
            _Task.current_task().set_parameter(VisionX.PARAM_NAME, token)

        self.token = token

    def samples(self) -> Tuple[List[str], List[Frame]]:
        _samples, targets = [], []
        task_anno_zips = ProjectAnnoDownloader(self.format, self.token, self.timeout)

        for anno_zip in task_anno_zips:
            task_samples = self.get_samples(anno_zip)

            for sample, target in task_samples:
                _samples.append(sample)
                targets.append(target)

        return _samples, targets

    def create_dataset(
        self,
        samples: List[str],
        targets: List[Frame],
    ) -> str:
        dataset_dir = Path(tempfile.mkdtemp())
        same_filename_cnt: Dict[str, int] = defaultdict(int)
        im_dir = dataset_dir.joinpath('images')
        im_dir.mkdir(parents=True, exist_ok=True)

        for sample in samples:
            im_file = im_dir.joinpath(Path(sample).name)

            if im_file.exists():
                same_filename_cnt[im_file.name] += 1
                im_file = im_file.parent.joinpath(f'{im_file.stem}_{same_filename_cnt[im_file.name]}{im_file.suffix}')

            shutil.move(sample, im_file)

        for i, target in enumerate(targets):
            target.id = i

        label = Label(frames=targets)
        label.tofile(str(dataset_dir.joinpath('annotations.xml')))
        return str(dataset_dir)

    # def get_samples(
    #     self,
    #     anno_zip: str,
    # ) -> List[Tuple[str, Frame]]:
    #     anno_dir = Path(anno_zip).with_suffix('')
    #     anno_dir.mkdir(parents=True, exist_ok=True)

    #     with zipfile.ZipFile(anno_zip, 'r') as zr:
    #         zr.extractall(str(anno_dir))

    #     Path(anno_zip).unlink()

    #     anno_file = anno_dir.joinpath('annotations.xml')
    #     im_dir = anno_dir.joinpath('images')
    #     label = Label.fromfile(str(anno_file))
    #     samples = []

    #     for frame in label.frames:
    #         samples.append((str(im_dir.joinpath(frame.name)), frame))

    #     return samples

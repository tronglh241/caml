import shutil
from .. import Format
from pathlib import Path
from .label import Label, Frame
from typing import List, Tuple
import tempfile
from collections import defaultdict


class CVAT(Format):
    def samples(self) -> List[Tuple[str, Frame]]:
        im_dir = Path(self.data_dir).joinpath('images')
        anno_file = Path(self.data_dir).joinpath('annotations.xml')
        label = Label.fromfile(str(anno_file))
        _samples = []

        for frame in label.frames:
            im_file = str(im_dir.joinpath(frame.name))
            _samples.append((im_file, frame))

        return _samples

    @staticmethod
    def merge(samples: List[Tuple[str, Frame]]) -> str:
        data_dir = Path(tempfile.mkdtemp())
        im_dir = data_dir.joinpath('images')
        anno_file = data_dir.joinpath('annotations.xml')

        frames = []
        same_filename_cnt = defaultdict(int)

        for im_file, frame in samples:
            im_file_p = Path(im_file)

            if im_file_p.name in same_filename_cnt:
                same_filename_cnt[im_file_p.name] += 1
                im_outfile = im_dir.joinpath(f'{im_file_p.stem}_{same_filename_cnt[im_file_p.name]}{im_file_p.suffix}')

            shutil.move(im_file, str(im_outfile))
            frames.append(frame)

        Label(frames).tofile(str(anno_file))

        return str(data_dir)

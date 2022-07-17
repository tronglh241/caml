import shutil
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from ..format import Format, register_format
from .label import Frame, Label


@register_format(name='CVAT for images 1.1')
class CVAT(Format):
    def samples(self) -> List[Tuple[str, Frame]]:
        data_dir = Path(self.data_dir)
        im_dir = data_dir.joinpath('images')
        anno_file = data_dir.joinpath('annotations.xml')
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
        im_dir.mkdir()

        frames = []
        same_filename_cnt: Dict[str, int] = defaultdict(int)

        for i, (im_file, frame) in enumerate(samples):
            im_outfile = im_dir.joinpath(Path(im_file).name)

            if im_outfile.exists():
                same_filename_cnt[im_outfile.name] += 1
                im_outfile = im_dir.joinpath(
                    f'{im_outfile.stem}_{same_filename_cnt[im_outfile.name]}{im_outfile.suffix}',
                )

            shutil.move(im_file, str(im_outfile))

            frame.id = i
            frames.append(frame)

        Label(frames).tofile(str(anno_file))

        return str(data_dir)

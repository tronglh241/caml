import shutil
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from ..format import Format, register_format
from .label import Label


@register_format(name='COCO Keypoint for Monash 1.0')
class COCO(Format):
    def samples(self) -> List[Tuple[str, Label]]:
        data_dir = Path(self.data_dir)
        im_dir = data_dir.joinpath('images')
        anno_file = data_dir.joinpath('annotations', 'person_keypoints_monash_default.json')
        label = Label.fromfile(str(anno_file))
        _samples = []

        for frame in label.iter():
            im_file = str(im_dir.joinpath(frame.images[0].file_name))
            _samples.append((im_file, frame))

        return _samples

    @staticmethod
    def merge(samples: List[Tuple[str, Label]]) -> str:
        data_dir = Path(tempfile.mkdtemp())
        im_dir = data_dir.joinpath('images')
        anno_file = data_dir.joinpath('annotations', 'person_keypoints_monash_default.json')
        im_dir.mkdir()

        frames = []
        same_filename_cnt: Dict[str, int] = defaultdict(int)

        for im_file, frame in samples:
            im_outfile = im_dir.joinpath(frame.images[0].file_name)

            if im_outfile.exists():
                same_filename_cnt[im_outfile.name] += 1
                im_outfile = im_dir.joinpath(
                    f'{im_outfile.stem}_{same_filename_cnt[im_outfile.name]}{im_outfile.suffix}',
                )

            im_outfile.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(im_file, str(im_outfile))
            frames.append(frame)

        Label.merge(frames).tofile(str(anno_file))

        return str(data_dir)

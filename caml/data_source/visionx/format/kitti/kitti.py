import shutil
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from ..format import Format, register_format


@dataclass
class KittiLabel:
    calib: Dict[str, str]
    image: Dict[str, str]
    label: Dict[str, str]


@register_format(name='KITTI 3D Detection 1.0')
class KITTI(Format):
    def samples(self) -> List[Tuple[str, KittiLabel]]:
        data_dir = Path(self.data_dir)
        pcd_dir = data_dir.joinpath('velodyne')
        _samples = []

        for pcd_file in sorted(pcd_dir.glob('*')):
            image = {im_file.parent.name: str(im_file)
                     for im_file in data_dir.glob(f'image*/{pcd_file.stem}*')}
            label = {label_file.parent.name: str(label_file)
                     for label_file in data_dir.glob(f'label*/{pcd_file.stem}*')}
            calib = {calib_file.parent.name: str(calib_file)
                     for calib_file in data_dir.glob(f'calib*/{pcd_file.stem}*')}

            _samples.append((str(pcd_file), KittiLabel(calib, image, label)))

        return _samples

    @staticmethod
    def merge(samples: List[Tuple[str, KittiLabel]]) -> str:
        data_dir = Path(tempfile.mkdtemp())
        pcd_dir = data_dir.joinpath('velodyne')
        pcd_dir.mkdir()

        same_filename_cnt: Dict[str, int] = defaultdict(int)

        for pcd_file, kitti_label in samples:
            pcd_outfile = pcd_dir.joinpath(Path(pcd_file).name)

            if pcd_outfile.exists():
                same_filename_cnt[pcd_outfile.name] += 1
                pcd_outfile = pcd_dir.joinpath(
                    f'{pcd_outfile.stem}_{same_filename_cnt[pcd_outfile.name]}{pcd_outfile.suffix}',
                )

            pcd_outfile.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(pcd_file, str(pcd_outfile))

            for calib_dirname, calib_file in kitti_label.calib.items():
                calib_outfile = data_dir.joinpath(calib_dirname, f'{pcd_outfile.stem}{Path(calib_file).suffix}')
                calib_outfile.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(calib_file, str(calib_outfile))

            for image_dirname, image_file in kitti_label.image.items():
                image_outfile = data_dir.joinpath(image_dirname, f'{pcd_outfile.stem}{Path(image_file).suffix}')
                image_outfile.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(image_file, str(image_outfile))

            for label_dirname, label_file in kitti_label.label.items():
                label_outfile = data_dir.joinpath(label_dirname, f'{pcd_outfile.stem}{Path(label_file).suffix}')
                label_outfile.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(label_file, str(label_outfile))

        return str(data_dir)

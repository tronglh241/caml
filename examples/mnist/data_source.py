import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from torchvision.datasets import MNIST

from caml.data_source import DataSource


class MNISTSource(DataSource):
    def __init__(
        self,
        split: str = 'train',
    ):
        super(MNISTSource, self).__init__()
        if split not in ['train', 'test']:
            raise ValueError('`split` must be `train` or `test`')

        self.split = split

    def samples(self) -> Tuple[list, Optional[list]]:
        dataset = MNIST(download=True, root=tempfile.gettempdir(), train=self.split == 'train')
        tmp_dir = Path(tempfile.mkdtemp())
        tmp_dir.mkdir(parents=True, exist_ok=True)

        im_files = []
        numbers = []

        for img, number in dataset:
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
                img.save(f, format='JPEG')

            im_files.append(f.name)
            numbers.append(number)

        return im_files, numbers

    def create_dataset(
        self,
        samples: list,
        targets: list = None,
    ) -> str:
        tmp_dir = Path(tempfile.mkdtemp())
        tmp_dir.mkdir(parents=True, exist_ok=True)

        for i, sample in enumerate(samples):
            if targets:
                target = targets[i]
                outdir = tmp_dir.joinpath(str(target))
                outdir.mkdir(parents=True, exist_ok=True)
                shutil.move(sample, outdir)
            else:
                shutil.move(sample, tmp_dir)

        return str(tmp_dir)

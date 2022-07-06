import random
from pathlib import Path

from caml.dataset import Dataset


class MNISTDataset(Dataset):
    def __init__(
        self,
        path: str = None,
        id_: str = None,
    ):
        super(MNISTDataset, self).__init__(path=path, id_=id_)

    def X(self) -> list:
        return self._X

    def y(self) -> list:
        return self._y

    def load_dataset(
        self,
        path: str,
    ) -> None:
        im_files = []
        numbers = []

        imgs = list(Path(path).glob('*/*.jpg'))
        random.shuffle(imgs)

        for im_file in imgs:
            im_files.append(im_file)
            numbers.append(int(im_file.parent.name))

        self._X = im_files
        self._y = numbers

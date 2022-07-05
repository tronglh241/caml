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
        im_paths = []
        numbers = []

        for im_file in Path(path).glob('*/*.jpg'):
            im_paths.append(im_file)
            numbers.append(int(im_file.parent.name))

        self._X = im_paths
        self._y = numbers

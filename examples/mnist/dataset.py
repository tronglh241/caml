import tempfile
from pathlib import Path

from torchvision.datasets import MNIST

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

    def load_dataset(self, path: str) -> None:
        dataset = MNIST(download=False, root=path, train=True)
        tmp_dir = Path(tempfile.gettempdir()).joinpath('MNIST')
        tmp_dir.mkdir(parents=True, exist_ok=True)

        im_paths = []
        numbers = []

        for img, number in dataset:
            _, im_file = tempfile.mkstemp(suffix='.jpg', dir=str(tmp_dir))
            img.save(str(im_file))

            im_paths.append(im_file)
            numbers.append(number)

        self._X = im_paths
        self._y = numbers

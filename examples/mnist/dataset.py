from pathlib import Path

from caml.dataset import Dataset
from caml.data_source.visionx.format.cvat.label import Label


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
        data_dir = Path(path)
        im_dir = data_dir.joinpath('images')
        anno_file = data_dir.joinpath('annotations.xml')

        label = Label.fromfile(str(anno_file))

        for frame in label.frames:
            im_file = im_dir.joinpath(frame.name)
            number = int(frame.instances[0].label)

            if not im_file.exists():
                raise FileNotFoundError(str(im_file))

            im_files.append(im_file)
            numbers.append(number)

        self._X = im_files
        self._y = numbers

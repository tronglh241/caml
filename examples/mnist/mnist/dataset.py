from typing import Callable, List, Tuple, Union

import torch
from PIL import Image
from torch.utils.data import Dataset


class MNISTDataset(Dataset):
    def __init__(
        self,
        im_files: List[str],
        numbers: List[int] = None,
        transform: Callable = None,
    ):
        super(MNISTDataset, self).__init__()
        self.im_files = im_files
        self.numbers = numbers
        self.transform = transform

        if self.numbers is not None:
            assert len(self.im_files) == len(self.numbers)

    def __len__(self) -> int:
        return len(self.im_files)

    def __getitem__(self, idx: int) -> Union[Tuple[torch.Tensor], Tuple[torch.Tensor, int]]:
        im_file = self.im_files[idx]
        img = Image.open(im_file).convert('L')

        if self.transform:
            img = self.transform(img)

        if self.numbers is not None:
            number = self.numbers[idx]
            return img, number
        else:
            return img,

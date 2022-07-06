from caml.dataset import Dataset


class UnnamedDataset(Dataset):
    def __init__(self, path: str = None, id_: str = None):
        super(UnnamedDataset, self).__init__(path=path, id_=id_)

    def X(self) -> list:
        pass

    def y(self) -> list:
        pass

    def load_dataset(self, path: str) -> None:
        pass

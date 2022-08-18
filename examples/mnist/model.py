from typing import Any, Optional, Tuple

import torch
from mnist import main
from mnist.dataset import MNISTDataset
from mnist.net import MNISTNet
from torch.nn import NLLLoss
from torch.optim import SGD
from torch.utils.data import DataLoader
from torchvision import transforms

from caml.model import EvalModel, TrainModel


def get_data_loader(
    X: list,
    y: list = None,
    **kwargs: Any,
) -> DataLoader:
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    dataset = MNISTDataset(
        im_files=X,
        numbers=y,
        transform=transform,
    )

    loader = DataLoader(dataset, **kwargs)
    return loader


class MNISTTrainModel(TrainModel):
    def __init__(
        self,
        lr: float = 0.01,
        momentum: float = 0.9,
        num_epochs: int = 100,
        train_ratio: float = 0.8,
        path: str = None,
        id_: str = None,
        **data_loader_kwargs: Any,
    ):
        super(MNISTTrainModel, self).__init__(path=path, id_=id_)
        self.model = MNISTNet()
        self.optimizer = SGD(self.model.parameters(), lr=lr, momentum=momentum)
        self.criterion = NLLLoss()
        self.num_epochs = num_epochs
        self.data_loader_kwargs = data_loader_kwargs
        self.train_ratio = train_ratio
        self.best_checkpoint = None

    def fit(
        self,
        X: list,
        y: list,
    ) -> None:
        train_loader, val_loader = self.get_data_loaders(X, y, self.train_ratio, **self.data_loader_kwargs)

        self.best_checkpoint = main.train(
            model=self.model,
            train_loader=train_loader,
            val_loader=val_loader,
            optimizer=self.optimizer,
            criterion=self.criterion,
            log_interval=50,
            epochs=self.num_epochs,
        )

    def load_model(self, path: str) -> None:
        self.model.load_state_dict(torch.load(path))

    def best_model(self) -> Optional[str]:
        return self.best_checkpoint

    def get_data_loaders(
        self,
        X: list,
        y: list,
        train_ratio: float,
        **kwargs: Any,
    ) -> Tuple[DataLoader, DataLoader]:
        train_split_X = X[:round(len(X) * train_ratio)]
        train_split_y = y[:round(len(y) * train_ratio)]
        val_split_X = X[round(len(X) * train_ratio):]
        val_split_y = y[round(len(X) * train_ratio):]

        train_loader = get_data_loader(train_split_X, train_split_y, shuffle=True, **kwargs)
        val_loader = get_data_loader(val_split_X, val_split_y, shuffle=False, **kwargs)

        return train_loader, val_loader


class MNISTEvalModel(EvalModel):
    def __init__(
        self,
        path: str = None,
        id_: str = None,
        **data_loader_kwargs: Any,
    ):
        super(MNISTEvalModel, self).__init__(path=path, id_=id_)
        self.model = MNISTNet()
        self.data_loader_kwargs = data_loader_kwargs
        self.model.eval()

    def predict(
        self,
        X: list,
    ) -> list:
        loader = get_data_loader(X, **self.data_loader_kwargs)
        preds = []

        with torch.no_grad():
            for img, in iter(loader):
                pred = self.model(img)
                pred = pred.argmax(dim=1)
                preds.extend(pred.tolist())

        return preds

    def predict_proba(
        self,
        X: list,
    ) -> list:
        loader = get_data_loader(X, **self.data_loader_kwargs)
        preds = []

        with torch.no_grad():
            for img, in iter(loader):
                pred = self.model(img)
                preds.extend(pred.tolist())

        return preds

    def eval(
        self,
        X: list,
        y: list,
    ) -> Tuple[str, float]:
        assert len(X) == len(y)
        pred = self.predict(X)
        n_trues = sum([_pred == _y for _pred, _y in zip(pred, y)])
        acc = n_trues / len(y)
        return 'accuracy', acc

    def load_model(self, path: str) -> None:
        self.model.load_state_dict(torch.load(path))

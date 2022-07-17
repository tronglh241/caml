from pathlib import Path

from torchvision.datasets import MNIST
from tqdm import tqdm

from caml.data_source.visionx.format.cvat import SourceType, Tag
from caml.data_source.visionx.format.cvat.label import Frame, Label

dataset = MNIST(
    root='data_tmp',
    train=False,
    download=True,
)

data_dir = Path('MNIST_Test')
data_dir.mkdir(parents=True, exist_ok=True)

im_dir = data_dir.joinpath('images')
im_dir.mkdir(parents=True, exist_ok=True)

frames = []

for i, (img, number) in tqdm(list(enumerate(dataset))):
    im_name = f'{i:06d}.jpg'
    img.save(str(im_dir.joinpath(im_name)))
    frame = Frame(
        id_=i,
        name=im_name,
        width=img.width,
        height=img.height,
        instances=[
            Tag(label=str(number), source=SourceType.manual)
        ],
    )
    frames.append(frame)

Label(frames).tofile(str(data_dir.joinpath('annotations.xml')))

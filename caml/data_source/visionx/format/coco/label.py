from __future__ import annotations

import json
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

from .annotation import Annotation
from .base import Element
from .category import Category
from .image import Image
from .info import Info
from .license import License


class Label(Element):
    def __init__(
        self,
        images: List[Image],
        annotations: List[Annotation],
        categories: List[Category],
        info: Info = None,
        licenses: List[License] = None,
    ):
        super(Label, self).__init__()
        self.info = info
        self.licenses = licenses
        self.images = images
        self.annotations = annotations
        self.categories = categories

    @classmethod
    def parse(
        cls,
        label: dict,
    ) -> Label:
        images = [Image.parse(image) for image in label['images']]
        annotations = [Annotation.parse(annotation) for annotation in label['annotations']]
        categories = [Category.parse(category) for category in label['categories']]
        info: Optional[Info] = None
        licenses: Optional[List[License]] = None

        if 'info' in label:
            info = Info.parse(label['info'])

        if 'licenses' in label:
            licenses = [License.parse(license) for license in label['licenses']]

        return cls(images, annotations, categories, info, licenses)

    @property
    def json(self) -> dict:
        label: dict = {}

        if self.info:
            label['info'] = self.info.json

        if self.licenses:
            label['licenses'] = [license.json for license in self.licenses]

        label['images'] = [image.json for image in self.images]
        label['annotations'] = [annotation.json for annotation in self.annotations]
        label['categories'] = [category.json for category in self.categories]

        return label

    @classmethod
    def fromfile(
        cls,
        file_path: str,
    ) -> Label:
        with open(file_path, mode='r', encoding='utf-8') as f:
            label = json.load(f)

        return cls.parse(label)

    def tofile(
        self,
        file_path: str,
    ) -> None:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(self.json, f, indent=4)

    @staticmethod
    def merge(
        labels: List[Label],
    ) -> Label:
        if not len(labels):
            raise ValueError('`labels` is empty.')

        for i in range(len(labels) - 1):
            if not labels[i].mergeable(labels[i + 1]):
                raise ValueError('Labels are not mergeable.')

        images: List[Image] = []
        annotations: List[Annotation] = []

        for label in tqdm(labels, desc='Merging labels', leave=False):
            image_map = {}

            for image in label.images:
                image = deepcopy(image)
                image_map[image.id] = len(images)
                image.id = image_map[image.id]
                images.append(image)

            for annotation in label.annotations:
                annotation = deepcopy(annotation)
                annotation.image_id = image_map[annotation.image_id]
                annotation.id = len(annotations)
                annotations.append(annotation)

        merged_label = Label(
            images,
            annotations,
            deepcopy(labels[0].categories),
            deepcopy(labels[0].info),
            deepcopy(labels[0].licenses),
        )

        return merged_label

    def mergeable(
        self,
        other: Label,
    ) -> bool:
        if (self.info is None) != (other.info is None):
            return False

        if (self.licenses is None) != (other.licenses is None):
            return False

        if self.info is not None and other.info is not None and not self.info.equals(other.info):
            return False

        if self.licenses is not None and other.licenses is not None:
            for s_license in self.licenses:
                if not any((s_license.equals(o_license) for o_license in other.licenses)):
                    return False

        for s_category in self.categories:
            if not any((s_category.equals(o_category) for o_category in other.categories)):
                return False

        return True

    def iter(self) -> List[Label]:
        annos_by_im = defaultdict(list)
        labels = []

        for anno in self.annotations:
            annos_by_im[anno.image_id].append(anno)

        for image in self.images:
            images = [image]
            annotations = annos_by_im[image.id]

            label = Label(
                images,
                annotations,
                self.categories,
                self.info,
                self.licenses,
            )
            labels.append(label)

        return labels

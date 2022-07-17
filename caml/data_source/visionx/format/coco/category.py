from __future__ import annotations

from typing import List

from .base import Element


class Category(Element):
    def __init__(
        self,
        supercategory: str,
        id_: int,
        name: str,
        keypoints: List[str] = None,
        skeleton: List[List[int]] = None,
    ):
        super(Category, self).__init__()
        self.supercategory = supercategory
        self.id = id_
        self.name = name
        self.keypoints = keypoints
        self.skeleton = skeleton

    @classmethod
    def parse(
        cls,
        category: dict,
    ) -> Category:
        supercategory = category['supercategory']
        id_ = category['id']
        name = category['name']
        keypoints = category.get('keypoints')
        skeleton = category.get('skeleton')
        return cls(
            supercategory,
            id_,
            name,
            keypoints,
            skeleton,
        )

    @property
    def json(self) -> dict:
        category = {
            'supercategory': self.supercategory,
            'id': self.id,
            'name': self.name,
        }

        if self.keypoints:
            category['keypoints'] = self.keypoints

        if self.skeleton:
            category['skeleton'] = self.skeleton

        return category

    def equals(
        self,
        other: Category,
    ) -> bool:
        return (
            self.supercategory == other.supercategory
            and self.id == other.id
            and self.name == other.name
            and self.keypoints == other.keypoints
            and self.skeleton == other.skeleton
        )

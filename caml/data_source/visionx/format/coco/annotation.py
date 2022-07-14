from __future__ import annotations

from typing import List

from .base import Element


class BBox(Element):
    def __init__(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
    ):
        super(BBox, self).__init__()
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @classmethod
    def parse(
        cls,
        bbox: List[float],
    ) -> BBox:
        left, top, width, height = bbox
        return cls(
            left,
            top,
            width,
            height,
        )

    @property
    def json(self) -> List[float]:
        bbox = [
            self.left,
            self.top,
            self.width,
            self.height,
        ]
        return bbox


class Keypoint:
    def __init__(
        self,
        x: float,
        y: float,
        visibility: int,
    ):
        super(Keypoint, self).__init__()
        self.x = x
        self.y = y
        self.visibility = visibility


class Annotation(Element):
    def __init__(
        self,
        segmentation: List[List[int]],
        iscrowd: int,
        image_id: int,
        bbox: BBox,
        category_id: int,
        id_: int,
        area: float = None,
        attributes: dict = None,
        keypoints: List[Keypoint] = None,
        num_keypoints: int = None,
    ):
        super(Annotation, self).__init__()
        self.segmentation = segmentation
        self.iscrowd = iscrowd
        self.image_id = image_id
        self.bbox = bbox
        self.category_id = category_id
        self.id = id_
        self.area = area
        self.attributes = attributes
        self.keypoints = keypoints
        self.num_keypoints = num_keypoints

    @classmethod
    def parse(
        cls,
        annotation: dict,
    ) -> Annotation:
        segmentation = annotation['segmentation']
        iscrowd = annotation['iscrowd']
        image_id = annotation['image_id']
        bbox = BBox.parse(annotation['bbox'])
        category_id = annotation['category_id']
        id_ = annotation['id']
        area = annotation.get('area')
        attributes = annotation.get('attributes')
        num_keypoints = annotation.get('num_keypoints')

        if 'keypoints' in annotation:
            keypoints = [
                Keypoint(
                    annotation['keypoints'][i],
                    annotation['keypoints'][i + 1],
                    annotation['keypoints'][i + 2],
                )
                for i in range(0, len(annotation['keypoints']), 3)
            ]
        else:
            keypoints = None

        return cls(
            segmentation,
            iscrowd,
            image_id,
            bbox,
            category_id,
            id_,
            area,
            attributes,
            keypoints,
            num_keypoints,
        )

    @property
    def json(self) -> dict:
        annotation = {
            'segmentation': self.segmentation,
            'iscrowd': self.iscrowd,
            'image_id': self.image_id,
            'bbox': self.bbox.json,
            'category_id': self.category_id,
            'id': self.id,
        }

        if self.area:
            annotation['area'] = self.area

        if self.attributes:
            annotation['attributes'] = self.attributes

        if self.keypoints:
            keypoints = []

            for keypoint in self.keypoints:
                keypoints.extend([keypoint.x, keypoint.y, keypoint.visibility])

            annotation['keypoints'] = keypoints

        if self.num_keypoints:
            annotation['num_keypoints'] = self.num_keypoints

        return annotation

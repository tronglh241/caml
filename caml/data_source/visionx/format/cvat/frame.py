from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import List

from .base import Element
from .instance import Box, Cuboid, Instance, Points, Polygon, Polyline, Tag


class Frame(Element):
    tag = 'image'
    supported_instances = [
        Box,
        Cuboid,
        Points,
        Polygon,
        Polyline,
        Tag,
    ]

    def __init__(self, id_: int, name: str, width: int, height: int, instances: List[Instance]):
        super(Frame, self).__init__()
        self.id = id_
        self.name = name
        self.width = width
        self.height = height
        self.instances = instances

    @classmethod
    def parse(cls, frame: ET.Element) -> Frame:
        if frame.tag != cls.tag:
            raise RuntimeError(f'Incompatitable tag, {cls.tag} required, {frame.tag} found.')
        id_ = int(frame.attrib['id'])
        name = frame.attrib['name']
        width = int(frame.attrib['width'])
        height = int(frame.attrib['height'])

        instances = []

        for instance in frame:
            for supported_instance in cls.supported_instances:
                if instance.tag == supported_instance.tag:   # type: ignore
                    ins = supported_instance.parse(instance)  # type: ignore
                    instances.append(ins)

        return cls(id_, name, width, height, instances)

    @property
    def xml(self) -> ET.Element:
        attrib = {
            'id': str(self.id),
            'name': self.name,
            'width': str(self.width),
            'height': str(self.height),
        }
        ele = ET.Element(self.tag, attrib)
        ele.extend([instance.xml for instance in self.instances])
        return ele

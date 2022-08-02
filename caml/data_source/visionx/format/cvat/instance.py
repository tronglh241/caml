from __future__ import annotations

import xml.etree.ElementTree as ET
from enum import Enum
from typing import List

from .attrib import Attrib
from .base import Element


class Instance(Element):
    tag = ''

    @staticmethod
    def parse_attr(ele: ET.Element) -> List[Attrib]:
        attribs = [Attrib.parse(attrib) for attrib in ele]
        return attribs


class SourceType(Enum):
    manual = 'manual'
    auto = 'auto'


class Corner(Enum):
    xtl1 = 'xtl1'
    ytl1 = 'ytl1'
    xbl1 = 'xbl1'
    ybl1 = 'ybl1'
    xtr1 = 'xtr1'
    ytr1 = 'ytr1'
    xbr1 = 'xbr1'
    ybr1 = 'ybr1'
    xtl2 = 'xtl2'
    ytl2 = 'ytl2'
    xbl2 = 'xbl2'
    ybl2 = 'ybl2'
    xtr2 = 'xtr2'
    ytr2 = 'ytr2'
    xbr2 = 'xbr2'
    ybr2 = 'ybr2'


class Tag(Instance):
    tag = 'tag'

    def __init__(
        self,
        label: str,
        source: SourceType,
        attribs: List[Attrib] = None,
    ):
        super(Tag, self).__init__()
        self.label = label
        self.source = source
        self.attribs = attribs

    @classmethod
    def parse(cls, tag: ET.Element) -> Tag:
        label = tag.attrib['label']
        source = SourceType(tag.attrib['source'])
        attribs = cls.parse_attr(tag)
        return cls(label, source, attribs)

    @property
    def xml(self) -> ET.Element:
        attrib = {
            'label': self.label,
            'source': self.source.value,
        }
        ele = ET.Element(self.tag, attrib)

        if self.attribs:
            ele.extend([attrib.xml for attrib in self.attribs])

        return ele


class Box(Instance):
    tag = 'box'

    def __init__(
        self,
        label: str,
        occluded: bool,
        source: SourceType,
        z_order: bool,
        xtl: float,
        ytl: float,
        xbr: float,
        ybr: float,
        attribs: List[Attrib] = None,
    ):
        super(Box, self).__init__()
        self.label = label
        self.occluded = occluded
        self.source = source
        self.z_order = z_order
        self.xtl = xtl
        self.ytl = ytl
        self.xbr = xbr
        self.ybr = ybr
        self.attribs = attribs

    @classmethod
    def parse(cls, box: ET.Element) -> Box:
        label = box.attrib['label']
        occluded = bool(int(box.attrib['occluded']))
        source = SourceType(box.attrib['source'])
        z_order = bool(int(box.attrib['z_order']))
        xtl = float(box.attrib['xtl'])
        ytl = float(box.attrib['ytl'])
        xbr = float(box.attrib['xbr'])
        ybr = float(box.attrib['ybr'])
        attribs = cls.parse_attr(box)
        return cls(label, occluded, source, z_order, xtl, ytl, xbr, ybr, attribs)

    @property
    def xml(self) -> ET.Element:
        attrib = {
            'label': self.label,
            'occluded': str(int(self.occluded)),
            'source': self.source.value,
            'xtl': f'{self.xtl:.02f}',
            'ytl': f'{self.ytl:.02f}',
            'xbr': f'{self.xbr:.02f}',
            'ybr': f'{self.ybr:.02f}',
            'z_order': str(int(self.z_order)),
        }
        ele = ET.Element(self.tag, attrib)

        if self.attribs:
            ele.extend([attrib.xml for attrib in self.attribs])

        return ele


class Cuboid(Instance):
    tag = 'cuboid'

    def __init__(
        self,
        label: str,
        occluded: bool,
        source: SourceType,
        z_order: bool,
        xtl1: float,
        ytl1: float,
        xbl1: float,
        ybl1: float,
        xtr1: float,
        ytr1: float,
        xbr1: float,
        ybr1: float,
        xtl2: float,
        ytl2: float,
        xbl2: float,
        ybl2: float,
        xtr2: float,
        ytr2: float,
        xbr2: float,
        ybr2: float,
        face_top: List[Corner],
        face_bot: List[Corner],
        face_left: List[Corner],
        face_right: List[Corner],
        side_top: List[Corner],
        side_bot: List[Corner],
        side_back: List[Corner],
        attribs: List[Attrib] = None,
    ):
        super(Cuboid, self).__init__()
        self.label = label
        self.occluded = occluded
        self.source = source
        self.z_order = z_order
        self.xtl1 = xtl1
        self.ytl1 = ytl1
        self.xbl1 = xbl1
        self.ybl1 = ybl1
        self.xtr1 = xtr1
        self.ytr1 = ytr1
        self.xbr1 = xbr1
        self.ybr1 = ybr1
        self.xtl2 = xtl2
        self.ytl2 = ytl2
        self.xbl2 = xbl2
        self.ybl2 = ybl2
        self.xtr2 = xtr2
        self.ytr2 = ytr2
        self.xbr2 = xbr2
        self.ybr2 = ybr2
        self.face_top = face_top
        self.face_bot = face_bot
        self.face_left = face_left
        self.face_right = face_right
        self.side_top = side_top
        self.side_bot = side_bot
        self.side_back = side_back
        self.attribs = attribs

    @classmethod
    def parse(cls, box: ET.Element) -> Cuboid:
        label = box.attrib['label']
        occluded = bool(int(box.attrib['occluded']))
        source = SourceType(box.attrib['source'])
        z_order = bool(int(box.attrib['z_order']))
        xtl1 = float(box.attrib['xtl1'])
        ytl1 = float(box.attrib['ytl1'])
        xbl1 = float(box.attrib['xbl1'])
        ybl1 = float(box.attrib['ybl1'])
        xtr1 = float(box.attrib['xtr1'])
        ytr1 = float(box.attrib['ytr1'])
        xbr1 = float(box.attrib['xbr1'])
        ybr1 = float(box.attrib['ybr1'])
        xtl2 = float(box.attrib['xtl2'])
        ytl2 = float(box.attrib['ytl2'])
        xbl2 = float(box.attrib['xbl2'])
        ybl2 = float(box.attrib['ybl2'])
        xtr2 = float(box.attrib['xtr2'])
        ytr2 = float(box.attrib['ytr2'])
        xbr2 = float(box.attrib['xbr2'])
        ybr2 = float(box.attrib['ybr2'])
        face_top = [Corner(c) for c in box.attrib['face_top'].split(',')]
        face_bot = [Corner(c) for c in box.attrib['face_bot'].split(',')]
        face_left = [Corner(c) for c in box.attrib['face_left'].split(',')]
        face_right = [Corner(c) for c in box.attrib['face_right'].split(',')]
        side_top = [Corner(c) for c in box.attrib['side_top'].split(',')]
        side_bot = [Corner(c) for c in box.attrib['side_bot'].split(',')]
        side_back = [Corner(c) for c in box.attrib['side_back'].split(',')]
        attribs = cls.parse_attr(box)
        return cls(
            label,
            occluded,
            source,
            z_order,
            xtl1,
            ytl1,
            xbl1,
            ybl1,
            xtr1,
            ytr1,
            xbr1,
            ybr1,
            xtl2,
            ytl2,
            xbl2,
            ybl2,
            xtr2,
            ytr2,
            xbr2,
            ybr2,
            face_top,
            face_bot,
            face_left,
            face_right,
            side_top,
            side_bot,
            side_back,
            attribs,
        )

    @property
    def xml(self) -> ET.Element:
        attrib = {
            'label': self.label,
            'occluded': str(int(self.occluded)),
            'source': self.source.value,
            'xtl1': f'{self.xtl1}',
            'ytl1': f'{self.ytl1}',
            'xbl1': f'{self.xbl1}',
            'ybl1': f'{self.ybl1}',
            'xtr1': f'{self.xtr1}',
            'ytr1': f'{self.ytr1}',
            'xbr1': f'{self.xbr1}',
            'ybr1': f'{self.ybr1}',
            'xtl2': f'{self.xtl2}',
            'ytl2': f'{self.ytl2}',
            'xbl2': f'{self.xbl2}',
            'ybl2': f'{self.ybl2}',
            'xtr2': f'{self.xtr2}',
            'ytr2': f'{self.ytr2}',
            'xbr2': f'{self.xbr2}',
            'ybr2': f'{self.ybr2}',
            'face_top': ','.join([c.value for c in self.face_top]),
            'face_bot': ','.join([c.value for c in self.face_bot]),
            'face_left': ','.join([c.value for c in self.face_left]),
            'face_right': ','.join([c.value for c in self.face_right]),
            'side_top': ','.join([c.value for c in self.side_top]),
            'side_bot': ','.join([c.value for c in self.side_bot]),
            'side_back': ','.join([c.value for c in self.side_back]),
            'z_order': str(int(self.z_order)),
        }
        ele = ET.Element(self.tag, attrib)

        if self.attribs:
            ele.extend([attrib.xml for attrib in self.attribs])

        return ele


class Points(Instance):
    tag = 'points'

    def __init__(
        self,
        label: str,
        occluded: bool,
        source: SourceType,
        z_order: bool,
        points: List[List[float]],
        attribs: List[Attrib] = None,
    ):
        super(Points, self).__init__()
        self.label = label
        self.occluded = occluded
        self.source = source
        self.z_order = z_order
        self.points = points
        self.attribs = attribs

    @classmethod
    def parse(cls, box: ET.Element) -> Points:
        label = box.attrib['label']
        occluded = bool(int(box.attrib['occluded']))
        source = SourceType(box.attrib['source'])
        z_order = bool(int(box.attrib['z_order']))
        points = [[float(p) for p in point.split(',')] for point in box.attrib['points'].split(';')]
        attribs = cls.parse_attr(box)
        return cls(label, occluded, source, z_order, points, attribs)

    @property
    def xml(self) -> ET.Element:
        attrib = {
            'label': self.label,
            'occluded': str(int(self.occluded)),
            'source': self.source.value,
            'points': ';'.join([','.join([f'{p:.02f}' for p in point]) for point in self.points]),
            'z_order': str(int(self.z_order)),
        }
        ele = ET.Element(self.tag, attrib)

        if self.attribs:
            ele.extend([attrib.xml for attrib in self.attribs])

        return ele


class Polygon(Points):
    tag = 'polygon'


class Polyline(Points):
    tag = 'polyline'

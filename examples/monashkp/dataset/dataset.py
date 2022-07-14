# from collections import defaultdict
# from pathlib import Path
# from typing import Dict

# from caml.data_source.visionx import cvat
# from caml.dataset import Dataset

# from . import coco


# class UnnamedDataset(Dataset):
#     def __init__(self, path: str = None, id_: str = None):
#         super(UnnamedDataset, self).__init__(path=path, id_=id_)

#     def X(self) -> list:
#         label = coco.Label.fromfile(self.anno_file)
#         im_dir = Path(self.im_dir)
#         im_files = [str(im_dir.joinpath(image.file_name)) for image in label.images]
#         return im_files

#     def y(self) -> list:
#         label = coco.Label.fromfile(self.anno_file)
#         item_by_im: Dict[int, list] = defaultdict(list)

#         for item in label.iter():
#             item_by_im[item.images[0].id] = item

#         items = [item_by_im[image.id] for image in label.images]

#         return items

#     def load_dataset(self, path: str) -> None:
#         im_dir = Path(path).joinpath('images')

#         if im_dir.exists():
#             self.im_dir = str(im_dir)
#         else:
#             raise FileNotFoundError(f'{im_dir} does not exists.')

#         cvlabel = cvat.Label.fromfile(str(im_dir.joinpath('annotations.xml')))
#         images = []
#         annotations = []
#         anno_id_map = {}

#         for frame in cvlabel.frames:
#             image = coco.Image(
#                 license=0,
#                 file_name=frame.name,
#                 coco_url='',
#                 height=frame.height,
#                 width=frame.width,
#                 date_captured='',
#                 flickr_url='',
#                 id_=frame.id,
#             )
#             images.append(image)

#             for instance in frame.instances:
#                 if instance.label not in anno_id_map:
#                     anno_id_map[instance.label] = len(anno_id_map)

#                 if instance.tag == cvat.Box.tag:
#                     annotation = coco.Annotation(
#                         segmentation=[],
#                         iscrowd=0,
#                         image_id=frame.id,
#                         bbox=coco.BBox(
#                             left=instance.xtl,
#                             top=instance.ytl,
#                             width=instance.xbr - instance.xtl,
#                             height=instance.ybr - instance.ytl,
#                         ),
#                         category_id=anno_id_map[instance.label],
#                         id_=coco.Annotation,
#                         attributes={attrib.name: attrib.value for attrib in instance.attribs},
#                     )
#                 elif instance.tag == cvat.Point.tag:
#                     annotation = coco.Annotation(
#                         segmentation=[],
#                         iscrowd=0,
#                         image_id=frame.id,
#                         bbox=coco.BBox(
#                             left=instance.xtl,
#                             top=instance.ytl,
#                             width=instance.xbr - instance.xtl,
#                             height=instance.ybr - instance.ytl,
#                         ),
#                         category_id=anno_id_map[instance.label],
#                         id_=coco.Annotation,
#                         keypoints=[coco.Keyfor point in instance.points],
#                         num_keypoints: int = None,
#                     )

#                 coco.Annotation += 1

#         cclabel = coco.Label(
#             images,
#             annotations: List[Annotation],
#             categories: List[Category],
#             info: Info = None,
#             licenses: List[License] = None,
#         )

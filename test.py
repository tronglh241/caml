from clearml import Task

from caml.data_source.visionx.visionx import VisionX

Task.init('Test', 'test')


source = VisionX(task_ids=[30323], format_='COCO Keypoint for Monash 1.0')
samples, targets = source.samples()
data_dir = source.create_dataset(samples, targets)
breakpoint()

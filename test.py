from clearml import Task
from caml.data_source.visionx.visionx import VisionX

Task.init('Test', 'test')


source = VisionX(project_id=45)
samples, targets = source.samples()
data_dir = source.create_dataset(samples, targets)
breakpoint()

import argparse
from pathlib import Path

import yaml

from .task.dl import EvalTask, TrainTask
from .task.task import Task

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['train', 'eval'])
    parser.add_argument('cfg_file')

    args = parser.parse_args()

    with open(args.cfg_file) as f:
        config = yaml.safe_load(f)

    requirement_file = str(Path(args.cfg_file).with_name('requirements.txt'))

    if args.cmd == 'train':
        task: Task = TrainTask(requirement_file=requirement_file, **config['train'])
    elif args.cmd == 'eval':
        task = EvalTask(requirement_file=requirement_file, **config['eval'])

    task.run()

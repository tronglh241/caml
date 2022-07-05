import argparse

import yaml

from .task.data.query import DataQueryTask
from .task.dl import EvalTask, TrainTask
from .task.task import Task

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['train', 'eval', 'query'])
    parser.add_argument('cfg_file')
    parser.add_argument('requirement_file')

    args = parser.parse_args()

    with open(args.cfg_file) as f:
        config = yaml.safe_load(f)

    if args.cmd == 'train':
        task: Task = TrainTask(requirement_file=args.requirement_file, **config)
    elif args.cmd == 'eval':
        task = EvalTask(requirement_file=args.requirement_file, **config)
    else:
        task = DataQueryTask(requirement_file=args.requirement_file, **config)

    task.run()

from __future__ import annotations

import argparse
import os
import warnings
from enum import Enum
from pathlib import Path
from typing import List

import yaml

from .task.dl import EvalTask, TrainTask
from .task.query import DataQueryTask
from .task.task import Task

REQUIREMENT_FILE = 'requirements.txt'


class Cmd(str, Enum):
    TRAIN = 'train'
    EVAL = 'eval'
    QUERY = 'query'
    INIT = 'init'

    @classmethod
    def choices(cls) -> List[Cmd]:
        cs = [
            cls.TRAIN,
            cls.EVAL,
            cls.QUERY,
            cls.INIT,
        ]
        return cs

    def __str__(self) -> str:
        return self.value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=Cmd.choices())
    parser.add_argument('--cfg-file')
    parser.add_argument('--requirement-file')
    parser.add_argument('--dir')

    args = parser.parse_args()

    if args.cmd == Cmd.INIT:
        template_dir = Path(__file__).with_name('template')

        if args.dir:
            target_dir = Path(args.dir)

            if target_dir.exists():
                raise FileExistsError(f'{target_dir} already exists.')

            target_dir.mkdir(parents=True)
        else:
            target_dir = Path(args.dir)

        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(template_dir)):
            _dir = target_dir.joinpath(Path(dirpath).relative_to(template_dir))

            if i:
                _dir.mkdir()

            for filename in filenames:
                with Path(dirpath).joinpath(filename).open(mode='r') as fr:
                    with _dir.joinpath(Path(filename).stem).open(mode='w') as fw:
                        fw.write(fr.read())
    else:
        if args.cfg_file:
            cfg_file = args.cfg_file
        else:
            cfg_file = Path(os.getcwd()).joinpath('config', f'{args.cmd}.yml')

        with open(cfg_file) as f:
            config = yaml.safe_load(f)

        if args.requirement_file:
            requirement_file = args.requirement_file
        else:
            requirement_file_p = Path(os.getcwd()).joinpath(REQUIREMENT_FILE)

            if requirement_file_p.exists():
                requirement_file = str(requirement_file_p)
            else:
                warnings.warn('Cannot find requirement file.')

        if args.cmd == Cmd.TRAIN:
            task: Task = TrainTask(**config, requirement_file=requirement_file)
        elif args.cmd == Cmd.EVAL:
            task = EvalTask(**config, requirement_file=requirement_file)
        elif args.cmd == Cmd.QUERY:
            task = DataQueryTask(**config, requirement_file=requirement_file)

        task.run()

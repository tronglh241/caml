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
TEMPLATE_SUFFIX = '-tpl'


class Cmd(str, Enum):
    @classmethod
    def choices(cls) -> List[Cmd]:
        cs = [c.value for c in cls._member_map_.values()]
        return cs

    def __str__(self) -> str:
        return self.value


class InitCmd(Cmd):
    INIT = 'init'


class ExecCmd(Cmd):
    TRAIN = 'train'
    EVAL = 'eval'
    QUERY = 'query'


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=InitCmd.choices())
    parser.add_argument('directory', nargs='?')
    args = parser.parse_args()

    if args.cmd == InitCmd.INIT:
        template_dir = Path(__file__).with_name('template')

        if args.directory:
            target_dir = Path(args.directory)

            if target_dir.exists():
                raise FileExistsError(f'{target_dir} already exists.')

            target_dir.mkdir(parents=True)
        else:
            target_dir = Path(os.getcwd())

        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(template_dir)):
            _dir = target_dir.joinpath(Path(dirpath).relative_to(template_dir))

            if i:
                _dir.mkdir()

            for filename in filenames:
                with Path(dirpath).joinpath(filename).open(mode='r') as fr:
                    with _dir.joinpath(Path(filename).name.replace(TEMPLATE_SUFFIX, '')).open(mode='w') as fw:
                        fw.write(fr.read())


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=ExecCmd.choices())
    parser.add_argument('cfg_file', nargs='?')
    parser.add_argument('requirement_file', nargs='?')
    args = parser.parse_args()

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
        requirement_file = str(requirement_file_p)

        if not requirement_file_p.exists():
            warnings.warn('Cannot find requirement file.')

    if args.cmd == ExecCmd.TRAIN:
        task: Task = TrainTask(**config, requirement_file=requirement_file)
    elif args.cmd == ExecCmd.EVAL:
        task = EvalTask(**config, requirement_file=requirement_file)
    elif args.cmd == ExecCmd.QUERY:
        task = DataQueryTask(**config, requirement_file=requirement_file)

    task.run()

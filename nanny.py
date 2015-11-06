#!C:/Python27/python
# -*- coding: utf-8 -*-
import os
import argparse
import uuid
from nannies import enabled_nannies, health
from nanny_util import info, tell


def file_exists(filepath):
    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        msg = 'Cannot find file {filepath}'.format(filepath=filepath)
        raise argparse.ArgumentTypeError(msg)
    return filepath


def watch(filepath):
    uid = str(uuid.uuid4())
    for nanny in enabled_nannies:
        nanny(filepath, uid).start()


def stat(task):
    stats = health.HealthNanny.stat(task)
    if stats is None:
        info('Task {task} was not found.'.format(task=task))
    else:
        tell(stats)


def json(task):
    stats = health.HealthNanny.json(task)
    if stats is None:
        info('Task {task} was not found.'.format(task=task))
    else:
        tell(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nanny watches after your cheeky Python programs.')
    parser.add_argument(dest='filepath', metavar='path_to_task', type=file_exists, nargs='?', help='run task with nanny')
    parser.add_argument('--stat', help='show stats by task name', dest='stat', metavar='task_name')
    parser.add_argument('--json', help='full stats by task name in json', dest='json', metavar='task_name')

    args = parser.parse_args()

    if args.stat:
        stat(args.stat)
    elif args.json:
        json(args.json)
    elif args.filepath:
        watch(args.filepath)
    else:
        parser.print_help()

# -*- coding: utf-8 -*-
from datetime import datetime


def tell(text):
    print '\033[1;37m{text}\033[1;m'.format(text=text)


def info(text):
    print '\033[1;36m{text}\033[1;m\033[1;37m'.format(text=text)


def warn(text):
    print '\033[1;31m{text}\033[1;m\033[1;37m'.format(text=text)


def parse_time(s):
    return datetime.strptime(s.split('.')[0], '%Y-%m-%d %H:%M:%S')

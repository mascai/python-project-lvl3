# -*- coding:utf-8 -*-

import os
import re
from urllib.parse import urlparse


def get_filename(url):
    return '{}.html'.format(to_safe_path(url))


def get_dirname(url):
    return '{}_files'.format(to_safe_path(url))


def get_file(resource_url):
    """ Get filename with extension"""
    path, extension = os.path.splitext(resource_url)
    return '{}{}'.format(to_safe_path(path), extension)


def to_safe_path(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc.strip('/')
    path = parsed_url.path.strip('/')

    path_to = os.path.join(host, path)
    return re.sub(r'[^\w]+', '-', path_to)

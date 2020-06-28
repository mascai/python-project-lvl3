# -*- coding:utf-8 -*-

"""Module with requests."""
import logging
import requests
import os
from urllib.parse import urljoin
from progress.bar import Bar
from bs4 import BeautifulSoup

import page_loader.url  # noqa WPS301


logger = logging.getLogger(__name__)


def parse_url(url, path_to_save_dir):
    logger.debug("Start parsing {}".format(url))
    page_content = get_content(url)
    path = page_loader.url.get_dirname(url)
    links, content_for_save = get_links(page_content, path)
    with Bar('Saving', max=len(links) + 2) as progress:
        file_name = page_loader.url.get_filename(url)
        path_to_save_file = os.path.join(path_to_save_dir, file_name)
        save_data(content_for_save, path_to_save_file)
        progress.next()

        content_dir = os.path.join(path_to_save_dir, path)
        logger.debug('Create directory {} for content'.format(content_dir))
        create_directory(content_dir)
        progress.next()

        logger.debug('Saving content')
        save_content(links, url, content_dir, progress.next,)


def save_data(content_for_save, path_to_file):
    try:
        mode = 'w' if isinstance(content_for_save, str) else 'wb'
        with open(path_to_file, mode) as f:
            f.write(content_for_save)
    except OSError as save_err:
        logger.error('Save error: {}'.format(save_err))
        raise LoaderError() from save_err


def create_directory(path_to_resource_dir: str):
    try:
        if not os.path.exists(path_to_resource_dir):
            os.mkdir(path_to_resource_dir)
    except OSError as create_dir_err:
        logger.error('Create resource dir error: {}'.format(create_dir_err))
        raise LoaderError() from create_dir_err


def save_content(links, url, path_to_resources_dir, on_progress):
    for link, name in links.items():
        file_content = get_content(urljoin(url, link))
        path = os.path.join(path_to_resources_dir, name)
        save_data(file_content, path)
        on_progress()


def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logger.error('Invalid response. {}'.format(err))
        raise LoaderError() from err
    return response.content


def get_links(page_content, resource_dir_name):
    soup = BeautifulSoup(page_content, 'html.parser')
    links = {}
    patterns = [
        ('script', 'src'),
        ('link', 'href'),
        ('img', 'src'),
    ]
    for tag, attr in patterns:
        for item in soup.find_all(tag):
            link = item.get(attr)
            if need_to_be_downloaded(link):
                path = page_loader.url.get_file(link)
                item[attr] = '{}/{}'.format(resource_dir_name, path)
                links[link] = path

    return links, str(soup)


def need_to_be_downloaded(link):
    if link is None:
        return False
    return link.startswith('/') and os.path.splitext(link)[-1] != ''


class LoaderError(Exception):
    """Base class for exceptions """

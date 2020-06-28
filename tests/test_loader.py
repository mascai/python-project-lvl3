# -*- coding:utf-8 -*-

import os
import tempfile
import pytest
from requests_mock import Mocker()

from page_loader import loader

RESOURCE_URL = 'https://test.test/user/test/main-page/'


def test_save_url(simple_page_content):
    with Mocker() as mock:
        mock.get(RESOURCE_URL, text=simple_page_content)

        with tempfile.TemporaryDirectory() as tmpdirname:
            loader.parse_url(RESOURCE_URL, tmpdirname)
            assert len(os.listdir(tmpdirname)) != 0

            files_path = [
                os.path.join(tmpdirname, file_name)
                for file_name in os.listdir(tmpdirname)
            ]
            file_path, = list(filter(os.path.isfile, files_path))

            with open(file_path, 'r') as file_descriptor:
                file_content = file_descriptor.read()
                assert file_content == simple_page_content


def test_save_url_with_fetch_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(loader.LoaderError):
            loader.parse_url(RESOURCE_URL, tmpdirname)


def test_save_url_with_tmpdir_err(simple_page_content):
    with Mocker() as mock:
        mock.get(RESOURCE_URL, text=simple_page_content)
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(loader.LoaderError):
                fake_dir = '{}_fake_34213'.format(tmpdirname)
                loader.parse_url(RESOURCE_URL, fake_dir)


EXPECTED_LINKS = { # noqa WPS407
    '/assets/js/main.js': 'assets-js-main.js',
    '/css/styles.css': 'css-styles.css',
    '/image.png': 'image.png',
}


def test_get_resource_links(page_with_links_content):
    resource_dir_name = 'test-resource-dir_files'

    links, replace_content = loader.get_links(
        page_with_links_content, resource_dir_name,
    )

    assert EXPECTED_LINKS == links
    for path in links.values():
        expected_link = os.path.join(resource_dir_name, path)
        assert expected_link in replace_content


@pytest.mark.parametrize(
    'link,expected',
    [
        ('/assets/main.js', True),
        ('/assets/styles.css', True),
        ('/static/logo.png', True),
        ('https://cdn2.domain.io/dist.js', False),
        ('/user/info', False),
        ('', False),
        (' ', False),
    ],
)
def test_need_to_be_downloaded(link, expected):
    result = loader.need_to_be_downloaded(link)
    assert result == expected

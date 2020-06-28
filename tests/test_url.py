# -*- coding:utf-8 -*-

from page_loader import url


def test_to_filename():
    expected = 'hexlet-io-courses.html'
    result = url.get_filename('https://hexlet.io/courses')
    assert expected == result


def test_to_resource_dirname():
    expected = 'hexlet-io-courses_files'
    result = url.get_dirname('https://hexlet.io/courses')
    assert expected == result


def test_to_resource():
    expected = 'assets-application.css'
    result = url.get_file('/assets/application.css')
    assert expected == result

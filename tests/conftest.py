# -*- coding:utf-8 -*-
import pytest


@pytest.fixture
def simple_page_content():
    with open('tests/fixtures/simple_page.html') as f:
        yield f.read()


@pytest.fixture
def page_with_links_content():
    with open('tests/fixtures/page_with_links.html') as f:
        yield f.read()

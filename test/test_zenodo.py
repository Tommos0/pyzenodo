#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from pyzenodo import zenodo


@pytest.fixture(autouse=True)
def zen():
    return zenodo.Zenodo('123')


def test_find_by_githup_repo(zen):
    assert zen.find_by_github_repo('NLeSC/eSalsa-MPI') is not None
    assert zen.find_by_github_repo('eSalsa') is None
    assert zen.find_by_github_repo('SomeRandom/Repo') is None


def test_search(zen):
    assert zen.search('eSalsa') is not None
    assert str(zen.search('dfgsdgflkjsdfglkj')) == '[]'


def test_search_eq_github_search(zen):
    assert str(zen.search('eSalsa')[0]) == str(zen.find_by_github_repo('NLeSC/eSalsa-MPI'))

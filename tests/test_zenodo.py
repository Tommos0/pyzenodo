#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from pyzenodo import zenodo


@pytest.fixture(autouse=True)
def zen():
    return zenodo.Zenodo('123_i_dont_need_no_key')


def test_find_by_githup_repo(zen):
    assert zen.find_by_github_repo('NLeSC/eSalsa-MPI') is not None
    assert zen.find_by_github_repo('eSalsa') is None
    assert zen.find_by_github_repo('SomeRandom/Repo') is None


def test_search(zen):
    assert zen.search('eSalsa') is not None
    assert str(zen.search('dfgsdgflkjsdfglkj')) == '[]'


def test_search_eq_github_search(zen):
    assert str(zen.search('eSalsa')[0]) == str(zen.find_by_github_repo('NLeSC/eSalsa-MPI'))


def test_get_versions_for_record(zen):
    record = zen.find_by_github_repo('NLeSC/eSalsa-MPI')
    versions = record.get_versions()
    assert len(versions) > 2
    for version in versions:
        assert version['recid'] is not None
        assert version['name'] is not None
        assert version['doi'] is not None and 'zenodo' in version['doi']
        assert version['date'] is not None

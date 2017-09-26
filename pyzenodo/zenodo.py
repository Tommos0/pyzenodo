# -*- coding: utf-8 -*-

__version__ = '1.0.0-alpha'

import requests
import re

try:
    import urlparse
    from urllib import urlencode
except ImportError:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

base_url = 'https://zenodo.org/api/'

class Zenodo(object):
    def __init__(self, api_key=''):
        self._api_key = api_key
        self.re_github_repo = re.compile(r'.*github.com/(.*?/.*?)[/$]')

    def search(self, search):
        search = search.replace('/', ' ')  # zenodo can't handle '/' in search query
        params = {'q': search}
        return self._get_records(params)['hits']['hits']

    def _extract_github_repo(self, identifier):
        matches = self.re_github_repo.match(identifier)
        if matches:
            return matches.group(1)
        return None

    def find_by_github_repo(self, search):
        records = self.search(search)
        for record in records:
            if 'metadata' not in record or 'related_identifiers' not in record['metadata']:
                continue
            for identifier in [identifier['identifier'] for identifier in record['metadata']['related_identifiers']]:
                repo = self._extract_github_repo(identifier)
                if repo and repo.upper() == search.upper():
                    return record
        return None

    def _get_records(self, params):
        url = base_url + 'records?' + urlparse.urlencode(params)
        return requests.get(url).json()


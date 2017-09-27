# -*- coding: utf-8 -*-


import requests
import re

from bs4 import BeautifulSoup

try:
    import urlparse
    from urllib import urlencode
except ImportError:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

base_url = 'https://zenodo.org/api/'


class Record(object):
    data = None

    def __init__(self, data):
        self.data = data

    @staticmethod
    def _row_to_version(row):
        link = row.select('a')[0]
        texts = row.select('small')
        recid = re.match(r'/record/(\d*)', link.attrs['href']).group(1)
        return {
            'recid' : recid,
            'name'  : link.text,
            'doi'   : texts[0].text,
            'date'  : texts[1].text,
            'original_version' : Zenodo.get_record(recid).original_version()
        }

    def get_versions(self):
        """Get version details from Zenodo webpage (it is not available in the REST api)"""
        res = requests.get('https://zenodo.org/record/'+self.data['conceptrecid'])
        soup = BeautifulSoup(res.text, 'html.parser')
        version_rows = soup.select('.well.metadata > table.table tr')
        if len(version_rows) == 0:  # when only 1 version
            return [{
                'recid': self.data['id'],
                'name': '1',
                'doi': self.data['doi'],
                'date': self.data['created'],
                'original_version': self.original_version()
            }]
        return [self._row_to_version(row) for row in version_rows if len(row.select('td')) > 1]

    def original_version(self):
        for identifier in self.data['metadata']['related_identifiers']:
            if identifier['relation'] == 'isSupplementTo':
                return re.match(r'.*/tree/(.*$)', identifier['identifier']).group(1)
        return None

    def __str__(self):
        return str(self.data)


class Zenodo(object):
    def __init__(self, api_key=''):
        self._api_key = api_key
        self.re_github_repo = re.compile(r'.*github.com/(.*?/.*?)[/$]')

    def search(self, search):
        """search Zenodo record for string `search`

        :param search: string to search
        :return: Record[] results
        """
        search = search.replace('/', ' ')  # zenodo can't handle '/' in search query
        params = {'q': search}
        return self._get_records(params)

    def _extract_github_repo(self, identifier):
        matches = self.re_github_repo.match(identifier)
        if matches:
            return matches.group(1)
        return None

    def find_record_by_github_repo(self, search):
        records = self.search(search)
        for record in records:
            if 'metadata' not in record.data or 'related_identifiers' not in record.data['metadata']:
                continue
            for identifier in [identifier['identifier'] for identifier in record.data['metadata']['related_identifiers']]:
                repo = self._extract_github_repo(identifier)
                if repo and repo.upper() == search.upper():
                    return record
        return None

    @staticmethod
    def get_record(recid):
        url = base_url + 'records/' + recid
        return Record(requests.get(url).json())

    @staticmethod
    def _get_records(params):
        url = base_url + 'records?' + urlencode(params)
        return [Record(hit) for hit in requests.get(url).json()['hits']['hits']]

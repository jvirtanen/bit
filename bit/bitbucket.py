#
# Copyright 2019 Bit authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import typing

from . import git
from . import http


class PullRequest(typing.NamedTuple):
    identifier: int
    title: str


def _parse_pull_request(value: typing.Dict[str, typing.Any]) -> PullRequest:
    return PullRequest(value['id'], value['title'])


API_BASE_URL = 'https://api.bitbucket.org/2.0'

WEB_BASE_URL = 'https://bitbucket.org'


class Client:


    def __init__(self, username: str, password: str):
        self._headers = {
            'Authorization': http.basic_auth(username, password)
        }


    def get_pull_requests(self, repository: str) -> typing.List[PullRequest]:
        query = '?fields=values.id,values.title'
        url = '{}/repositories/{}/pullrequests{}'.format(API_BASE_URL, repository, query)
        data = http.get_json(url, headers=self._headers)
        return [_parse_pull_request(value) for value in data['values']]


def repository(path: str = None) -> typing.Optional[str]:
    remotes = git.remote(path)
    return _preferred_repository(remotes) or _any_repository(remotes)


def repository_url(repository: str) -> str:
    return '{}/{}'.format(WEB_BASE_URL, repository)


PREFERRED_REMOTE_NAMES = ['upstream', 'bitbucket', 'origin']


def _preferred_repository(remotes: typing.Sequence[git.Remote]) -> typing.Optional[str]:
    remote_urls = {remote.name: remote.url for remote in remotes}
    for remote_name in PREFERRED_REMOTE_NAMES:
        remote_url = remote_urls.get(remote_name)
        if not remote_url:
            continue
        repository = _parse_repository(remote_url)
        if repository:
            return repository
    return None


def _any_repository(remotes: typing.Sequence[git.Remote]) -> typing.Optional[str]:
    for remote in remotes:
        repository = _parse_repository(remote.url)
        if repository:
            return repository
    return None


REMOTE_URL_PATTERNS = [
    r'git@bitbucket.org:(?P<repository>[^\.]+).git',
    r'https://bitbucket.org/(?P<repository>[^\.]+).git',
    r'https://\w+@bitbucket.org/(?P<repository>[^\.]+).git',
]


def _parse_repository(remote_url: str) -> typing.Optional[str]:
    for pattern in REMOTE_URL_PATTERNS:
        match = re.match(pattern, remote_url)
        if match:
            return match['repository']
    return None

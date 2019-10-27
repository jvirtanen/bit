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


BASE_URL = 'https://api.bitbucket.org/2.0'


class Client:


    def __init__(self, username: str, password: str):
        self._headers = {
            'Authorization': http.basic_auth(username, password)
        }


    def get_pull_requests(self, repository: str) -> typing.List[PullRequest]:
        query = '?fields=values.id,values.title'
        url = '{}/repositories/{}/pullrequests{}'.format(BASE_URL, repository, query)
        data = http.get_json(url, headers=self._headers)
        return [_parse_pull_request(value) for value in data['values']]


def repository(path: str = None) -> typing.Optional[str]:
    for remote in git.remote(path):
        repository = _parse_repository(remote)
        if repository:
            return repository
    return None


def _parse_repository(remote: git.Remote) -> typing.Optional[str]:
    match = re.match(r'git@bitbucket.org:(?P<repository>[^\.]+).git', remote.url)
    if not match:
        return None
    return match['repository']

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

import sys
import typing

from . import bitbucket
from . import config
from . import git
from . import http


MAIN_USAGE = '''\
Usage: bit <command> [<args>]

Available commands:

    pr  List pull requests
\
'''


def main(args: typing.Sequence[str]) -> None:
    if args[:1] == ['pr']:
        pr(args[1:])
    else:
        _usage(MAIN_USAGE)


PR_USAGE = '''\
Usage: bit pr list\
'''


def pr(args: typing.Sequence[str]) -> None:
    if args[:1] == ['list']:
        pr_list()
    else:
        _usage(PR_USAGE)


def pr_list() -> None:
    try:
        _format_pull_requests(_client().get_pull_requests(_repository()))
    except http.HTTPError as e:
        _error(e)


def _format_pull_requests(pull_requests: typing.Sequence[bitbucket.PullRequest]) -> None:
    for pull_request in sorted(pull_requests, key=lambda pull_request: pull_request.identifier):
        _format_pull_request(pull_request)


def _format_pull_request(pull_request: bitbucket.PullRequest) -> None:
    identifier = '#{}'.format(pull_request.identifier)
    print('{:>8}  {}'.format(identifier, pull_request.title))


def _client() -> bitbucket.Client:
    try:
        credentials = config.load()
    except config.ConfigError as e:
        _error(e)
    return bitbucket.Client(credentials.username, credentials.password)


def _repository() -> str:
    path = git.work_tree()
    repository = bitbucket.repository(path)
    if not repository:
        _error('not a Bitbucket repository')
    return repository


def _usage(message: str) -> typing.NoReturn:
    sys.exit(message)


def _error(message: typing.Union[str, Exception]) -> typing.NoReturn:
    sys.exit('error: {}'.format(message))

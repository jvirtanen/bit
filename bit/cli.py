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

import getopt
import sys
import typing
import webbrowser

from . import bitbucket
from . import config
from . import git
from . import http


BROWSE_USAGE = '''\
Usage: bit browse [-u|--url] [<user>/<repository>]\
'''


def browse(args: typing.Sequence[str]) -> None:
    browse = True
    opts, args = _getopt(args, 'hu', ['help', 'url'], BROWSE_USAGE)
    for opt, _ in opts:
        if opt in ['-h', '--help']:
            _usage(BROWSE_USAGE)
        elif opt in ['-u', '--url']:
            browse = False
    repository = args[0] if args else _repository()
    repository_url = bitbucket.repository_url(repository)
    if browse:
        _browse(repository_url)
    else:
        print(repository_url)


def pr_list(args: typing.Sequence[str]) -> None:
    try:
        _format_pull_requests(_client().get_pull_requests(_repository()))
    except http.HTTPError as e:
        _error(e)


PR_USAGE = '''\
Usage: bit pr list\
'''

PR_COMMANDS = {
    'list': pr_list,
}


def pr(args: typing.Sequence[str]) -> None:
    _run_command(args, PR_COMMANDS, PR_USAGE)


MAIN_USAGE = '''\
Usage: bit <command> [<args>]

Available commands:

    browse  Open a Bitbucket page in the default browser
    pr      List Bitbucket pull requests
\
'''

MAIN_COMMANDS = {
    'browse': browse,
    'pr': pr,
}


def main(args: typing.Sequence[str]) -> None:
    _run_command(args, MAIN_COMMANDS, MAIN_USAGE)


Command = typing.Callable[[typing.Sequence[str]], None]


def _run_command(args: typing.Sequence[str],
                 commands: typing.Mapping[str, Command], usage_message: str) -> None:
    if len(args) < 1:
        _usage(usage_message)
    command = commands.get(args[0])
    if not command:
        _usage(usage_message)
    command(args[1:])


def _getopt(args: typing.Sequence[str], shortopts: str, longopts: typing.Sequence[str],
            usage_message: str) -> typing.Tuple[typing.List[typing.Tuple[str, str]], typing.List[str]]:
    try:
        return getopt.getopt(list(args), shortopts, list(longopts))
    except getopt.GetoptError:
        _usage(usage_message)


def _browse(url: str) -> None:
    try:
        if not webbrowser.open(url):
            print(url)
    except webbrowser.Error:
        print(url)


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

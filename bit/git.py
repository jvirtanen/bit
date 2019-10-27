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

import os
import re
import subprocess
import typing


def work_tree() -> str:
    return os.environ.get('GIT_WORK_TREE', os.getcwd())


class Remote(typing.NamedTuple):
    name: str
    url: str
    url_type: str


def remote(path: str = None) -> typing.List[Remote]:
    output = subprocess.check_output(['git', 'remote', '--verbose'], cwd=path)
    remotes = [_parse_remote(line) for line in output.decode('utf-8').splitlines()]
    return [remote for remote in remotes if remote]


def _parse_remote(line: str) -> typing.Optional[Remote]:
    match = re.match(r'(?P<name>\w+)\s+(?P<url>[^\s]+)\s+\((?P<url_type>\w+)\)', line)
    if not match:
        return None
    return Remote(match['name'], match['url'], match['url_type'])

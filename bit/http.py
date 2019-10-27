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

import base64
import json
import typing
import urllib.error
import urllib.request


class HTTPError(Exception):
    pass


def basic_auth(username: str, password: str) -> str:
    credentials = '{}:{}'.format(username, password).encode('utf-8')
    return 'Basic {}'.format(base64.b64encode(credentials).decode('utf-8'))


def get_json(url: str, headers: typing.Dict[str, str] = None) -> typing.Any:
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request) as infile:
            return json.load(infile)
    except json.JSONDecodeError as e:
        raise HTTPError(e)
    except urllib.error.URLError as e:
        raise HTTPError(e)

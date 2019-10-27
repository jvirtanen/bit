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

import configparser
import getpass
import os
import stat
import typing


PATH = os.path.expanduser(os.path.join('~', '.config', 'bit'))


class ConfigError(Exception):
    pass


class Config(typing.NamedTuple):
    username: str
    password: str


def load() -> Config:
    if os.path.exists(PATH):
        config = _read(PATH)
    else:
        config = _prompt()
        _write(config, PATH)
    return config


def _read(path: str) -> Config:
    data = configparser.ConfigParser()
    try:
        with open(path, 'r') as infile:
            data.read_file(infile)
    except configparser.Error:
        _error(path, 'invalid file format')
    except OSError as e:
        _error(path, e.strerror)
    return _parse(data)


def _prompt() -> Config:
    username = input('Username: ')
    password = getpass.getpass('App password: ')
    return Config(username, password)


def _write(config: Config, path: str) -> None:
    data = _format(config)
    try:
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, 'w') as outfile:
            data.write(outfile)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        _error(path, e.strerror)


def _parse(data: configparser.ConfigParser) -> Config:
    username = data.get('default', 'username')
    password = data.get('default', 'password')
    return Config(username, password)


def _format(config: Config) -> configparser.ConfigParser:
    data = configparser.ConfigParser()
    data.add_section('default')
    data.set('default', 'username', config.username)
    data.set('default', 'password', config.password)
    return data


def _error(path: str, message: str) -> typing.NoReturn:
    raise ConfigError("{}: {}".format(path, message))

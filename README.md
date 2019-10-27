# Bit

Bit is a simple command line utility for working with [Bitbucket][].

  [Bitbucket]: https://bitbucket.org

Bit requires Git and Python 3.6.

## Installation

Install Bit with Python:
```
python setup.py install
```

> :warning: Bit is **not** yet available on the Python Package Index (PyPI) and
> must be installed from this repository.

## Usage

The first time Bit requires access to Bitbucket, it will ask for your username
and an app password. You can create an app password by navigating to _Bitbucket
settings_, _App passwords_ on the website.

List open pull requests:
```
bit pr list
```

## Development

Install Bit with Python for development:
```
python setup.py develop
```

## License

Copyright 2019 Bit authors.

Released under the Apache License, Version 2.0. See `LICENSE.txt` for details.

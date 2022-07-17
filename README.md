# [Himon](<https://dc.fandom.com/wiki/Himon_(New_Earth)>)

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Himon.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Status](https://img.shields.io/pypi/status/Himon.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Version](https://img.shields.io/pypi/v/Himon.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - License](https://img.shields.io/pypi/l/Himon.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Black](https://img.shields.io/badge/Black-Enabled-000000?style=flat-square)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/Flake8-Enabled-informational?style=flat-square)](https://github.com/PyCQA/flake8)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Himon.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Himon/graphs/contributors)

[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Himon/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/Himon/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/Himon/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/Himon/actions/workflows/testing.yaml)

A [Python](https://www.python.org/) wrapper for [League of Comic Geeks](https://leagueofcomicgeeks.com).

## Installation

```bash
$ poetry add himon
```

## Example Usage

```python
from himon.league_of_comic_geeks import LeagueofComicGeeks
from himon.sqlite_cache import SQLiteCache

session = LeagueofComicGeeks(api_key="API Key", client_id="Client Id", cache=SQLiteCache())
```

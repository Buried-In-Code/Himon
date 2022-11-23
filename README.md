# Himon

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Himon.svg?logo=PyPI&label=Python&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Status](https://img.shields.io/pypi/status/Himon.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Version](https://img.shields.io/pypi/v/Himon.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - License](https://img.shields.io/pypi/l/Himon.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Hatch](https://img.shields.io/badge/Packaging-Hatch-4051b5?logo=hatch&style=flat-square)](https://github.com/pypa/hatch)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/Code--Style-Black-000000?style=flat-square)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/Imports-isort-informational?style=flat-square)](https://pycqa.github.io/isort/)
[![Flake8](https://img.shields.io/badge/Linter-Flake8-informational?style=flat-square)](https://github.com/PyCQA/flake8)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Himon.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Himon/graphs/contributors)
[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Himon/Code%20Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/Himon/actions/workflows/code-analysis.yaml)
[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/Himon/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/Himon/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/himon?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://himon.readthedocs.io/en/latest/?badge=latest)

A [Python](https://www.python.org/) wrapper for [League of Comic Geeks](https://leagueofcomicgeeks.com).

## Installation

### PyPI

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Install the library from [PyPI](https://pypi.org/project/himon): `pip install himon`

### Github

1. Make sure you have [Python](https://www.python.org/) installed: `python --version`
2. Clone the repo: `git clone https://github.com/Buried-In-Code/Himon`
3. Install the library: `pip install .`

## Example Usage

```python
from himon.league_of_comic_geeks import LeagueofComicGeeks
from himon.sqlite_cache import SQLiteCache

access_token = None
session = LeagueofComicGeeks(client_id="Client Id", client_secret="Client Secret", access_token=access_token, cache=SQLiteCache())

# Generate an access token if not supplied
if not access_token:
  session.access_token = session.generate_access_token()

# Search for Comic
for search in session.search(search_term="Blackest Night"):
    print(f"Search result: {search.publisher_name} - {search.series_name} - {search.title}")

# Get Series by id
series = session.series(series_id=100096)
print(f"Series: {series.series_id} - {series.title}")

# Get Comic by id
comic = session.comic(comic_id=2710631)
print(f"Comic: {comic.comic_id} - {comic.title}")
```

## Notes

Who or what is Himon?

> Himon is a citizen of New Genesis who secretly lives on the planet Apokolips, which is ruled by Darkseid.
>
> More details at [Himon (New Earth)](<https://dc.fandom.com/wiki/Himon_(New_Earth)>)

## Socials

[![Social - Discord](https://img.shields.io/badge/Discord-The--DEV--Environment-7289DA?logo=Discord&style=for-the-badge)](https://discord.gg/nqGMeGg)

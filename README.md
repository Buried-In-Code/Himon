# Himon

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Himon.svg?logo=Python&label=Python&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Status](https://img.shields.io/pypi/status/Himon.svg?logo=Python&label=Status&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Version](https://img.shields.io/pypi/v/Himon.svg?logo=Python&label=Version&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - License](https://img.shields.io/pypi/l/Himon.svg?logo=Python&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Hatch](https://img.shields.io/badge/Packaging-Hatch-4051b5?style=flat-square)](https://github.com/pypa/hatch)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?style=flat-square&logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Black](https://img.shields.io/badge/Code--Style-Black-000000?style=flat-square)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/Linter-Ruff-informational?style=flat-square)](https://github.com/charliermarsh/ruff)

[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Himon.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Himon/graphs/contributors)
[![Github Action - Testing](https://img.shields.io/github/actions/workflow/status/Buried-In-Code/Himon/testing.yaml?branch=main&logo=Github&label=Testing&style=flat-square)](https://github.com/Buried-In-Code/Himon/actions/workflows/testing.yaml)

[![Read the Docs](https://img.shields.io/readthedocs/himon?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://himon.readthedocs.io/en/latest/?badge=latest)

A [Python](https://www.python.org/) wrapper for [League of Comic Geeks](https://leagueofcomicgeeks.com).

## Installation

```bash
pip install Himon
```

## Documentation

[Read the project documentation](https://himon.readthedocs.io/en/latest/?badge=latest)

### Example Usage

```python
from himon.league_of_comic_geeks import LeagueofComicGeeks
from himon.sqlite_cache import SQLiteCache

session = LeagueofComicGeeks(client_id="Client Id", client_secret="Client Secret", access_token=None, cache=SQLiteCache())

# Generate an access token if not supplied
if not session.access_token:
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

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/Buried-In-Code/Himon/issues) to submit bugs or request features.

## Notes

Who or what is Himon?

> Himon is a citizen of New Genesis who secretly lives on the planet Apokolips, which is ruled by Darkseid.
>
> More details at [Himon (New Earth)](<https://dc.fandom.com/wiki/Himon_(New_Earth)>)

## Socials

[![Social - Matrix](https://img.shields.io/matrix/The-Dev-Environment:matrix.org?label=The%20Dev%20Environment&logo=matrix&style=for-the-badge)](https://matrix.to/#/#The-Dev-Environment:matrix.org)

# Himon

[![PyPI - Python](https://img.shields.io/pypi/pyversions/Himon.svg?logo=Python&label=Python&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Status](https://img.shields.io/pypi/status/Himon.svg?logo=Python&label=Status&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - Version](https://img.shields.io/pypi/v/Himon.svg?logo=Python&label=Version&style=flat-square)](https://pypi.python.org/pypi/Himon/)
[![PyPI - License](https://img.shields.io/pypi/l/Himon.svg?logo=Python&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)

[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye.astral.sh)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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
for result in session.search(search_term="Blackest Night"):
    print(f"Result: {result.publisher_name} - {result.series_name} - {result.title}")

# Get Series by id
series = session.get_series(series_id=100096)
print(f"Series: {series.id} - {series.title}")

# Get Comic by id
comic = session.get_comic(comic_id=2710631)
print(f"Comic: {comic.id} - {comic.title}")
```

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/Buried-In-Code/Himon/issues) to submit bugs or request features.

## Socials

[![Social - Matrix](https://img.shields.io/matrix/The-Dev-Environment:matrix.org?label=The%20Dev%20Environment&logo=matrix&style=for-the-badge)](https://matrix.to/#/#The-Dev-Environment:matrix.org)

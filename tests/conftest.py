"""The conftest module.

This module contains pytest fixtures.
"""

import os
from pathlib import Path

import pytest

from himon.league_of_comic_geeks import LeagueOfComicGeeks
from himon.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def client_id() -> str:
    """Retrieve the Client Id from environment variables."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__CLIENT_ID", default="IGNORED")


@pytest.fixture(scope="session")
def client_secret() -> str:
    """Retrieve the Client Secret from environment variables."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__CLIENT_SECRET", default="IGNORED")


@pytest.fixture(scope="session")
def access_token() -> str | None:
    """Retrieve the Access Token from environment variables."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__ACCESS_TOKEN")


@pytest.fixture(scope="session")
def session(client_id: str, client_secret: str, access_token: str | None) -> LeagueOfComicGeeks:
    """Set the Himon session fixture."""
    service = LeagueOfComicGeeks(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        cache=SQLiteCache(path=Path("tests/cache.sqlite"), expiry=None),
    )
    if not access_token:
        service.access_token = service.generate_access_token()
    return service

"""
The conftest module.

This module contains pytest fixtures.
"""
import os
from typing import Optional

import pytest

from himon.league_of_comic_geeks import LeagueofComicGeeks
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
def access_token() -> Optional[str]:
    """Retrieve the Access Token from environment variables."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__ACCESS_TOKEN")


@pytest.fixture(scope="session")
def session(client_id: str, client_secret: str, access_token: Optional[str]) -> LeagueofComicGeeks:
    """Set the Himon session fixture."""
    service = LeagueofComicGeeks(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        cache=SQLiteCache("tests/cache.sqlite", expiry=None),
    )
    if not access_token:
        service.access_token = service.generate_access_token()
    return service

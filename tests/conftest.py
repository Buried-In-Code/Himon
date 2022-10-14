"""
The conftest module.

This module contains pytest fixtures.
"""
import os

import pytest

from himon.league_of_comic_geeks import LeagueofComicGeeks
from himon.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def league_of_comic_geeks_api_key():
    """Set the League of Comic Geeks API key fixture."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__API_KEY", default="INVALID")


@pytest.fixture(scope="session")
def league_of_comic_geeks_client_id():
    """Set the League of Comic Geeks Client Id fixture."""
    return os.getenv("LEAGUE_OF_COMIC_GEEKS__CLIENT_ID", default="INVALID")


@pytest.fixture(scope="session")
def session(
    league_of_comic_geeks_api_key: str, league_of_comic_geeks_client_id: str
) -> LeagueofComicGeeks:
    """Set the Himon session fixture."""
    return LeagueofComicGeeks(
        api_key=league_of_comic_geeks_api_key,
        client_id=league_of_comic_geeks_client_id,
        cache=SQLiteCache("tests/cache.sqlite", expiry=None),
    )

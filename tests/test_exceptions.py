"""
The Exceptions test module.

This module contains tests for Exceptions.
"""
import pytest

from himon.exceptions import AuthenticationError, ServiceError
from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_unauthorized():
    """Test generating an AuthenticationError."""
    session = LeagueofComicGeeks(api_key="Invalid", client_id="Invalid", cache=None)
    with pytest.raises(AuthenticationError):
        session.comic(comic_id=1)


def test_not_found(session: LeagueofComicGeeks):
    """Test a 404 Not Found raises a ServiceError."""
    with pytest.raises(ServiceError):
        session._get_request(endpoint="/invalid")


def test_timeout(league_of_comic_geeks_api_key: str, league_of_comic_geeks_client_id: str):
    """Test a TimeoutError for slow responses."""
    session = LeagueofComicGeeks(
        api_key=league_of_comic_geeks_api_key,
        client_id=league_of_comic_geeks_client_id,
        timeout=0.1,
        cache=None,
    )
    with pytest.raises(ServiceError):
        session.comic(comic_id=1)

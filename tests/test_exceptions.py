"""
The Exceptions test module.

This module contains tests for Exceptions.
"""
from typing import Optional

import pytest

from himon.exceptions import AuthenticationError, ServiceError
from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_unauthorized():
    """Test generating an AuthenticationError."""
    session = LeagueofComicGeeks(
        client_id="Invalid", client_secret="Invalid", access_token=None, cache=None
    )
    with pytest.raises(AuthenticationError):
        session.comic(comic_id=1)


def test_not_found(session: LeagueofComicGeeks):
    """Test a 404 Not Found raises a ServiceError."""
    with pytest.raises(ServiceError):
        session._json_get_request(endpoint="/invalid")


def test_timeout(client_id: str, client_secret: str, access_token: Optional[str]):
    """Test a TimeoutError for slow responses."""
    session = LeagueofComicGeeks(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        timeout=0.1,
        cache=None,
    )
    with pytest.raises(ServiceError):
        session.comic(comic_id=1)

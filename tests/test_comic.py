"""
The Comic test module.

This module contains tests for Comic objects.
"""
from datetime import date, datetime

from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_comic(session: LeagueofComicGeeks):
    """Test using the comic endpoint with a valid comic_id."""
    result = session.comic(comic_id=2710631)
    assert result is not None
    assert result.comic_id == 2710631

    assert len(result.characters) == 106
    assert len(result.collected_in) == 13
    assert len(result.creators) == 9
    assert result.date_added == datetime(2012, 7, 2, 23, 15, 17)
    assert result.format == "Comic"
    assert result.is_enabled is True
    assert result.is_nsfw is False
    assert result.is_variant is False
    assert result.isbn is None
    assert len(result.key_events) == 0
    assert result.page_count == 48
    assert result.parent_id is None
    assert result.parent_title is None
    assert result.price == 3.99
    assert result.release_date == date(2009, 7, 15)
    assert result.sku == "MAY090106"
    assert result.title == "Blackest Night #1"
    assert result.upc == 76194128446000111
    assert len(result.variants) == 6


def test_character_null_publisher(session: LeagueofComicGeeks):
    """Test the comic endpoint with a comic that has a null character publisher name."""
    result = session.comic(comic_id=4174173)
    assert result is not None

    assert result.characters[0].publisher_name is None


def test_key_event_null_universe(session: LeagueofComicGeeks):
    """Test the comic endpoint with a comic that has a null key event universe name."""
    result = session.comic(comic_id=4174173)
    assert result is not None

    assert result.key_events[0].universe_name is None


def test_upc_alpha_only(session: LeagueofComicGeeks):
    """Test the comic endpoint with a comic that has an invalid character in the upc."""
    result = session.comic(comic_id=6257084)
    assert result is not None

    assert result.upc is None

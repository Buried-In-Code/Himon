"""The Comic test module.

This module contains tests for Comic objects.
"""

from datetime import date, datetime

from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_comic(session: LeagueofComicGeeks) -> None:
    """Test using the comic endpoint with a valid comic_id."""
    result = session.get_comic(comic_id=2710631)
    assert result is not None
    assert result.id == 2710631

    assert len(result.characters) == 185
    assert len(result.collected_in) == 1
    assert len(result.creators) == 8
    assert result.date_added.astimezone() == datetime(2012, 7, 2, 23, 15, 17).astimezone()
    assert result.format == "Comic"
    assert result.is_nsfw is False
    assert result.is_variant is False
    assert result.isbn is None
    assert len(result.keys) == 21
    assert result.page_count == 48
    assert result.parent_id is None
    assert result.parent_title is None
    assert result.price == 3.99
    assert result.release_date == date(2009, 7, 15)
    assert result.sku == "MAY090106"
    assert result.title == "Blackest Night #1"
    assert result.upc == 76194128446000111
    assert len(result.variants) == 7


def test_upc_alpha_only(session: LeagueofComicGeeks) -> None:
    """Test the comic endpoint with a comic that has an invalid character in the upc."""
    result = session.get_comic(comic_id=6257084)
    assert result is not None

    assert result.upc is None

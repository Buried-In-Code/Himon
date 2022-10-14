"""
The SearchResult test module.

This module contains tests for SearchResult objects.
"""
from datetime import date

from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_search_result(session: LeagueofComicGeeks):
    """Test using the search endpoint with a valid comic title."""
    results = session.search(search_term="Blackest Night #1")
    assert len(results) != 0
    result = [x for x in results if x.comic_id == 2710631][0]
    assert result is not None
    assert result.comic_id == 2710631

    assert result.format == "Comic"
    assert result.is_enabled is True
    assert result.is_variant is False
    assert result.parent_id is None
    assert result.parent_title is None
    assert result.price == 3.99
    assert result.publisher_id == 1
    assert result.publisher_name == "DC Comics"
    assert result.release_date == date(2009, 7, 15)
    assert result.series_id == 100096
    assert result.series_name == "Blackest Night"
    assert result.series_volume is None
    assert result.title == "Blackest Night #1"
    assert result.year_begin == 2009
    assert result.year_end == 2010

"""The SearchResult test module.

This module contains tests for SearchResult objects.
"""

from datetime import date
from decimal import Decimal

from himon.league_of_comic_geeks import LeagueOfComicGeeks
from himon.schemas.generic import ComicFormat


def test_search(session: LeagueOfComicGeeks) -> None:
    """Test using the search endpoint with a valid comic title."""
    results = session.search(search_term="Blackest Night #1")
    assert len(results) != 0
    result = next(x for x in results if x.id == 2710631)
    assert result is not None
    assert result.id == 2710631

    assert result.parent_id is None
    assert result.publisher_id == 1
    assert result.publisher_name == "DC Comics"
    assert result.series_id == 100096
    assert result.series_name == "Blackest Night"
    assert result.series_volume is None
    assert result.series_end == 2010
    assert result.series_begin == 2009
    assert result.title == "Blackest Night #1"
    assert result.parent_title is None
    assert result.date_release == date(2009, 7, 15)
    assert result.date_foc is None
    assert result.format == ComicFormat.COMIC
    assert result.is_variant is False
    assert result.price == Decimal("3.99")
    assert result.cover == 2
    assert result.count_pulls == 45
    assert result.is_enabled is True
    assert result.date_collected is None

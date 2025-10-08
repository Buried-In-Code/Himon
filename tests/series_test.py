"""The Series test module.

This module contains tests for Series objects.
"""

from datetime import datetime

from himon.league_of_comic_geeks import LeagueOfComicGeeks


def test_get_series(session: LeagueOfComicGeeks) -> None:
    """Test using the series endpoint with a valid series_id."""
    result = session.get_series(series_id=100096)
    assert result is not None
    assert result.id == 100096

    assert result.publisher_id == 1
    assert result.title == "Blackest Night"
    assert result.title_sort == "blackest night"
    assert result.volume is None
    assert result.year_begin == 2009
    assert result.year_end == 2010
    assert result.banner == 0
    assert result.cover_id == 2710631
    assert result.date_added == datetime(2012, 8, 5, 22, 20, 15)  # noqa: DTZ001
    assert result.is_enabled is True
    assert result.map_to_id == 0
    assert result.publisher_name == "DC Comics"
    assert result.publisher_slug == "dc"
    assert result.first_issue_id == 2710631
    assert result.type_id == 1
    assert result.language_id == 9
    assert result.series_string == "2009 - 2010"

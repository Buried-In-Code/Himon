"""The Series test module.

This module contains tests for Series objects.
"""

from datetime import datetime

from himon.league_of_comic_geeks import LeagueofComicGeeks


def test_series(session: LeagueofComicGeeks) -> None:
    """Test using the series endpoint with a valid series_id."""
    result = session.get_series(series_id=100096)
    assert result is not None
    assert result.id == 100096

    assert result.date_added.astimezone() == datetime(2012, 8, 5, 22, 20, 15).astimezone()
    assert result.publisher_id == 1
    assert result.publisher_name == "DC Comics"
    assert result.title == "Blackest Night"
    assert result.volume is None
    assert result.year_begin == 2009
    assert result.year_end == 2010

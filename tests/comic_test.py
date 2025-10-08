"""The Comic test module.

This module contains tests for Comic objects.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import HttpUrl

from himon.league_of_comic_geeks import LeagueOfComicGeeks
from himon.schemas.comic import CharacterType, KeyEventType
from himon.schemas.generic import ComicFormat, CoverType


def test_get_comic(session: LeagueOfComicGeeks) -> None:  # noqa: PLR0915
    """Test using the comic endpoint with a valid comic_id."""
    result = session.get_comic(comic_id=2710631)
    assert result is not None
    assert result.id == 2710631

    assert result.parent_id is None
    assert result.publisher_id == 1
    assert result.series_id == 100096
    assert result.title == "Blackest Night #1"
    assert result.date_release == date(2009, 7, 15)
    assert result.cover == 2
    assert result.format == ComicFormat.COMIC
    assert result.is_variant is False
    assert result.pages == 48
    assert result.price == Decimal("3.99")
    assert result.upc == 76194128446000111
    assert result.isbn is None
    assert result.sku == "MAY090106"
    assert result.sku_diamond == "MAY090106"
    assert result.sku_lunar is None
    assert result.is_nsfw is False
    assert result.consensus_users == 99
    assert result.count_votes == 0
    assert result.count_pulls == 45
    assert result.count_collected == 2259
    assert result.date_added == datetime(2012, 7, 2, 23, 15, 17)  # noqa: DTZ001
    assert result.is_enabled is True
    assert result.parent_title is None
    assert result.publisher_name == "DC Comics"
    assert result.publisher_slug == "dc"
    assert result.date_cover is None
    assert result.date_foc is None
    assert len(result.creators) >= 1
    assert result.creators[0].assoc_id == 6148534
    assert result.creators[0].id == 257
    assert result.creators[0].name == "Geoff Johns"
    assert result.creators[0].slug == "geoff-johns"
    assert result.creators[0].has_avatar is True
    assert result.creators[0].story_id == 1042882
    assert result.creators[0].role_id == "1"
    assert result.creators[0].role == "Writer"
    assert len(result.characters) >= 1
    assert result.characters[0].id == 42
    assert result.characters[0].tier_id == 4
    assert result.characters[0].parent_id == 41
    assert result.characters[0].individual_id == 41
    assert result.characters[0].name == "Flash"
    assert result.characters[0].has_avatar is True
    assert result.characters[0].avatar_comic_id is None
    assert result.characters[0].banner == 0
    assert result.characters[0].universe_id == 1
    assert result.characters[0].continuity_id is None
    assert result.characters[0].current_persona is None
    assert result.characters[0].slug is None
    assert result.characters[0].date_added == datetime(2018, 7, 22, 22, 34, 9)  # noqa: DTZ001
    assert result.characters[0].is_enabled is True
    assert result.characters[0].map_to_id == 0
    assert result.characters[0].character_type == CharacterType.MAIN
    assert result.characters[0].story_id == 1042882
    assert result.characters[0].parent_name == "Barry Allen"
    assert result.characters[0].avatar_id == 42
    assert result.characters[0].full_name == "Barry Allen as Flash"
    assert result.characters[0].universe_name == "Earth-0"
    assert result.characters[0].publisher_name == "DC Comics"
    assert result.characters[0].role_name == "Main"
    assert result.characters[0].role_note is None
    assert result.banner == HttpUrl(
        "https://s3.amazonaws.com/comicgeeks/comics/covers/large-2710631.jpg?1727669282"
    )
    assert len(result.keys) >= 1
    assert result.keys[0].id == 85011
    assert result.keys[0].comic_id == 2710631
    assert result.keys[0].key_event_type == KeyEventType.FIRST_APPEARANCE
    assert result.keys[0].type_id == 10164
    assert result.keys[0].note is None
    assert result.keys[0].string_primary == "First Appearance"
    assert result.keys[0].string_secondary is None
    assert result.keys[0].string_description == "Galius Zed as Black Lantern (Earth-0)"
    assert result.keys[0].character_id == 10164
    assert result.keys[0].name == "Black Lantern"
    assert result.keys[0].parent_name == "Galius Zed"
    assert result.keys[0].universe_name == "Earth-0"
    assert result.keys[0].universe_id == 1
    assert len(result.collected_in) >= 1
    assert result.collected_in[0].id == 5608951
    assert result.collected_in[0].parent_id is None
    assert result.collected_in[0].publisher_id == 1
    assert result.collected_in[0].publisher_name == "DC Comics"
    assert result.collected_in[0].series_id == 100096
    assert result.collected_in[0].series_name == "Blackest Night"
    assert result.collected_in[0].series_volume is None
    assert result.collected_in[0].series_end == 2010
    assert result.collected_in[0].series_begin == 2009
    assert result.collected_in[0].title == "Blackest Night: The Book of the Black HC"
    assert result.collected_in[0].parent_title is None
    assert result.collected_in[0].date_release == date(2021, 1, 19)
    assert result.collected_in[0].date_foc is None
    assert result.collected_in[0].format == ComicFormat.HARDCOVER
    assert result.collected_in[0].is_variant is False
    assert result.collected_in[0].price is None
    assert result.collected_in[0].cover == 2
    assert result.collected_in[0].count_pulls == 3
    assert result.collected_in[0].is_enabled is True
    assert result.collected_in[0].date_collected is None
    assert len(result.variants) >= 1
    assert result.variants[0].id == 1021704
    assert result.variants[0].title == "Blackest Night #1 1:25 Ethan Van Sciver Variant"
    assert result.variants[0].date_release == date(2009, 7, 15)
    assert result.variants[0].cover == 2
    assert result.variants[0].price == Decimal("3.99")
    assert result.variants[0].sku == "MAY090107"
    assert result.variants[0].date_foc is None
    assert result.variants[0].cover_type == CoverType.INCENTIVE
    assert len(result.covers) >= 1
    assert result.covers[0].id == 1021704
    assert result.covers[0].parent_id == 2710631
    assert result.covers[0].publisher_id == 1
    assert result.covers[0].publisher_name == "DC Comics"
    assert result.covers[0].series_id == 100096
    assert result.covers[0].series_name == "Blackest Night"
    assert result.covers[0].series_volume is None
    assert result.covers[0].series_end == 2010
    assert result.covers[0].series_begin == 2009
    assert result.covers[0].title == "Blackest Night #1 1:25 Ethan Van Sciver Variant"
    assert result.covers[0].parent_title == "Blackest Night #1"
    assert result.covers[0].date_release == date(2009, 7, 15)
    assert result.covers[0].date_foc is None
    assert result.covers[0].format == ComicFormat.COMIC
    assert result.covers[0].is_variant is True
    assert result.covers[0].price == Decimal("3.99")
    assert result.covers[0].cover == 2
    assert result.covers[0].count_pulls == 2
    assert result.covers[0].is_enabled is True
    assert result.covers[0].date_collected is None
    assert result.covers[0].cover_type == CoverType.INCENTIVE
    assert result.count_read == 3006


def test_upc_alpha_only(session: LeagueOfComicGeeks) -> None:
    """Test the comic endpoint with a comic that has an invalid character in the upc."""
    result = session.get_comic(comic_id=6257084)
    assert result is not None

    assert result.upc is None

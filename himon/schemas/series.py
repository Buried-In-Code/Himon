"""The Series module.

This module provides the following classes:

- Series
"""

__all__ = ["Series"]

from datetime import datetime
from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from himon.schemas import BaseModel
from himon.schemas._validators import ensure_bool, ensure_int, ensure_str


class Series(BaseModel):
    """The Series object contains information for a series.

    Attributes:
        banner:
        cover_id: ID to use as series cover.
        date_added: Date and time when the Series was added.
        date_modified: Date and time when the Series was last updated.
        description: Description of the Series.
        first_issue_id: ID of the first Issue in the Series.
        id: Identifier used by League of Comic Geeks.
        is_enabled:
        map_to_id:
        publisher_id: The publisher id of the Series.
        publisher_name: The publisher name of the Series.
        publisher_slug: The publisher name slugged to be usable in a url.
        series_string: String showing the year period for this Series.
        title: Name / Title of the Series.
        title_sort: The sort name of the Series.
        volume: Volume number.
        year_begin: The year the Series started.
        year_end: The year the Series ended.
    """

    banner: int
    cover_id: int = Field(alias="cover")
    date_added: datetime
    date_modified: datetime
    description: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    first_issue_id: int = Field(alias="comic_id")
    id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(ensure_bool)]
    map_to_id: int
    publisher_id: int
    publisher_name: str
    publisher_slug: str
    series_string: str
    title: str
    title_sort: str
    volume: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    year_begin: int
    year_end: Annotated[Optional[int], BeforeValidator(ensure_int)] = None

"""The Series module.

This module provides the following classes:

- Series
"""

from __future__ import annotations

__all__ = ["Series"]
from datetime import datetime

from pydantic import Field, field_validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_optional_int, to_optional_str


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
    description: str | None = None
    first_issue_id: int = Field(alias="comic_id")
    id: int
    map_to_id: int
    publisher_id: int
    publisher_name: str
    publisher_slug: str
    series_string: str
    title: str
    title_sort: str
    volume: int | None = None
    year_begin: int
    year_end: int | None = None

    @field_validator("volume", "year_end", mode="before")
    def _to_optional_int(cls: type[Series], v: str) -> int | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("description", mode="before")
    def _to_optional_str(cls: type[Series], v: str) -> str | None:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

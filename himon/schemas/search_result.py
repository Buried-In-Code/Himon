"""The Search Result module.

This module provides the following classes:

- SearchResult
"""
__all__ = ["SearchResult"]
from datetime import date, datetime
from typing import Optional, Type

from pydantic import Field, field_validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_bool, to_optional_float, to_optional_int, to_optional_str


class SearchResult(BaseModel):
    """The SearchResult object contains information for a search result.

    Attributes:
        date_modified: Date and time when the Comic was last updated.
        description: Description of the Comic.
        format: Type of Comic.
        id: Identifier used by League of Comic Geeks.
        is_enabled: Unknown field
        is_variant: Comic has been marked as Variant.
        parent_id: If it is a variant comic, id of the original comic.
        parent_title: If it is a variant comic, title of the original comic.
        price: Price of Comic.
        publisher_id: The publisher id of the Comic.
        publisher_name: The publisher name of the Comic.
        release_date: The date the Comic was released.
        series_id: The series id of the Comic.
        series_name: The series name of the Comic.
        series_volume: The series volume of the Comic.
        title: Name/Title of the Comic.
        year_begin: The year the Series started.
        year_end: The year the Series ended.
    """

    date_modified: datetime
    description: Optional[str] = None
    format: str  # noqa: A003
    id: int  # noqa: A003
    is_enabled: bool = Field(alias="enabled")
    is_variant: bool = Field(alias="variant")
    parent_id: Optional[int] = None
    parent_title: Optional[str] = None
    price: Optional[float] = None
    publisher_id: int
    publisher_name: str
    release_date: date = Field(alias="date_release")
    series_id: int
    series_name: str
    series_volume: Optional[int] = None
    title: str
    year_begin: int = Field(alias="series_begin")
    year_end: Optional[int] = Field(alias="series_end", default=None)

    @field_validator("parent_id", "series_volume", "year_end", mode="before")
    def _to_optional_int(cls: Type["SearchResult"], v: str) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("is_variant", "is_enabled", mode="before")
    def _to_bool(cls: Type["SearchResult"], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("price", mode="before")
    def _to_optional_float(cls: Type["SearchResult"], v: str) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

    @field_validator("description", "parent_title", mode="before")
    def _to_optional_str(cls: Type["SearchResult"], v: str) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

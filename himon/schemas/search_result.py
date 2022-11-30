"""
The Search Result module.

This module provides the following classes:

- SearchResult
"""
__all__ = ["SearchResult"]
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str


class SearchResult(BaseModel):
    """
    The SearchResult object contains information for a search result.

    Attributes:
        comic_id: Identifier used by League of Comic Geeks.
        date_modified: Date and time when the Comic was last updated.
        description: Description of the Comic.
        format: Type of Comic.
        is_enabled:
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

    comic_id: int = Field(alias="id")
    date_modified: datetime
    description: Optional[str] = None
    format: str
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

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("parent_id", "series_volume", "year_end", pre=True)
    def validate_optional_int(cls, v) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_variant", "is_enabled", pre=True)
    def validate_bool(cls, v) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

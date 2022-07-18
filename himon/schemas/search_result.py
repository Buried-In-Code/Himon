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
    """The SearchResult object contains information for a search result."""

    comic_id: int = Field(alias="id")  #: Identifier used in League of Comic Geeks
    date_modified: datetime  #: Date and time when the Comic was last updated.
    description: Optional[str] = None  #: Description of the Comic
    format: str  #: Type of Comic
    is_enabled: bool = Field(alias="enabled")
    is_variant: bool = Field(alias="variant")  #: Comic has been marked as Variant
    parent_id: Optional[int] = None  #: If it is a variant comic, Id of the original comic.
    parent_title: Optional[str] = None  #: If it is a variant comic, Title of the original comic.
    price: Optional[float] = None  #: Price of Comic.
    publisher_id: int  #: The publisher id of the Comic.
    publisher_name: str  #: The publisher name of the Comic.
    release_date: date = Field(alias="date_release")  #: The date the Comic was released.
    series_id: int  #: The series id of the Comic.
    series_name: str  #: The series name of the Comic.
    series_volume: Optional[int] = None  #: The series volume of the Comic.
    title: str  #: Name/Title of the Comic.
    year_begin: int = Field(alias="series_begin")  #: The year the Series started.
    year_end: Optional[int] = Field(alias="series_end", default=None)  #: The year the Series ended.

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("parent_id", "series_volume", "year_end", pre=True)
    def validate_optional_int(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_variant", "is_enabled", pre=True)
    def validate_bool(cls, v):
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v):
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

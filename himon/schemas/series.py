"""
The Series module.

This module provides the following classes:

- Series
"""
__all__ = ["Series"]
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_int, to_optional_str


class Series(BaseModel):
    """The Series object contains information for a series."""

    date_added: datetime  #: Date and time when the Series was added.
    date_modified: datetime  #: Date and time when the Series was last updated.
    description: Optional[str] = None  #: Description of the Series
    is_enabled: bool = Field(alias="enabled")
    publisher_id: int  #: The publisher id of the Series.
    publisher_name: str  #: The publisher name of the Series.
    series_id: int = Field(alias="id")  #: Identifier used in League of Comic Geeks
    title: str  #: Name/Title of the Series.
    volume: Optional[int] = None  #: Volume number
    year_begin: int  #: The year the Series started.
    year_end: Optional[int] = None  #: The year the Series ended.

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("description", pre=True)
    def validate_optional_str(cls, v):
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v):
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("volume", "year_end", pre=True)
    def validate_optional_int(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

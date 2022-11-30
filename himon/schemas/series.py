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
    """
    The Series object contains information for a series.

    Attributes:
        date_added: Date and time when the Series was added.
        date_modified: Date and time when the Series was last updated.
        description: Description of the Series.
        is_enabled:
        publisher_id: The publisher id of the Series.
        publisher_name: The publisher name of the Series.
        series_id: Identifier used by League of Comic Geeks.
        title: Name/Title of the Series.
        volume: Volume number.
        year_begin: The year the Series started.
        year_end: The year the Series ended.
    """

    date_added: datetime
    date_modified: datetime
    description: Optional[str] = None
    is_enabled: bool = Field(alias="enabled")
    publisher_id: int
    publisher_name: str
    series_id: int = Field(alias="id")
    title: str
    volume: Optional[int] = None
    year_begin: int
    year_end: Optional[int] = None

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("description", pre=True)
    def validate_optional_str(cls, v) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("volume", "year_end", pre=True)
    def validate_optional_int(cls, v) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

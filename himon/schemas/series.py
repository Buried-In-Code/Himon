"""
The Series module.

This module provides the following classes:

- Series
"""
__all__ = ["Series"]
from datetime import datetime
from typing import Optional

from pydantic import Field, validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_bool, to_optional_int, to_optional_str


class Series(BaseModel):
    """
    The Series object contains information for a series.

    Attributes:
        date_added: Date and time when the Series was added.
        date_modified: Date and time when the Series was last updated.
        description: Description of the Series.
        is_enabled: Unknown field
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

    @validator("description", pre=True)
    def _to_optional_str(cls, v: str) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("is_enabled", pre=True)
    def _to_bool(cls, v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("volume", "year_end", pre=True)
    def _to_optional_int(cls, v: str) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

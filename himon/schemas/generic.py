"""The Generic module.

This module provides the following classes:

- GenericComic
- GenericCover
"""

from __future__ import annotations

__all__ = ["GenericComic", "GenericCover"]
from datetime import date, datetime

from pydantic import Field, field_validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_bool, to_optional_float, to_optional_int, to_optional_str


class GenericComic(BaseModel):
    """The GenericIssue object contains the base for related/link issues.

    Attributes:
        cover:
        date_modified: Date and time when the Issue was last updated.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_variant: Issue has been marked as Variant.
        parent_id: If it is a variant Issue, id of the original Issue, else None.
        parent_title: If it is a variant Issue, title of the original Issue, else None.
        price: Price of the Issue.
        publisher_id: The publisher id of the Issue.
        publisher_name: The publisher name of the Issue.
        release_date: The date the Issue was released.
        series_begin: The year the Series started.
        series_end: The year the Series ended.
        series_id: Identifier used by League of Comic Geeks.
        series_name: Name / Title of the Series.
        series_volume: Series volume number.
        title: Name/Title of the Issue.
    """

    cover: int
    date_modified: datetime
    description: str | None = None
    format: str
    id: int
    is_variant: bool = Field(alias="variant")
    parent_id: int | None = None
    parent_title: str | None = None
    price: float | None = None
    publisher_id: int
    publisher_name: str
    release_date: date = Field(alias="date_release")
    series_begin: int
    series_end: int | None = None
    series_id: int
    series_name: str
    series_volume: int | None = None
    title: str

    @field_validator("is_variant", mode="before")
    def _to_bool(cls: type[GenericComic], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("price", mode="before")
    def _to_optional_float(cls: type[GenericComic], v: str) -> float | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

    @field_validator("parent_id", "series_volume", "series_end", mode="before")
    def _to_optional_int(cls: type[GenericComic], v: str) -> int | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("description", "parent_title", mode="before")
    def _to_optional_str(cls: type[GenericComic], v: str) -> str | None:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class GenericCover(GenericComic):
    """The GenericCover object extends GenericIssue by including the type of cover used.

    Attributes:
        cover_type:
    """

    cover_type: int

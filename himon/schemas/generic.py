"""The Generic module.

This module provides the following classes:

- GenericComic
- GenericCover
"""

__all__ = ["GenericComic", "GenericCover"]

from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import BeforeValidator, Field

from himon.schemas import BaseModel
from himon.schemas._validators import ensure_bool, ensure_date, ensure_float, ensure_int, ensure_str


class GenericComic(BaseModel):
    """The GenericIssue object contains the base for related/link issues.

    Attributes:
        cover:
        date_modified: Date and time when the Issue was last updated.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_collected:
        is_enabled:
        is_pulled:
        is_read:
        is_variant: Issue has been marked as Variant.
        is_wished:
        key_level:
        my_pick:
        my_rating:
        my_rating_dec:
        parent_id: If it is a variant Issue, id of the original Issue, else None.
        parent_title: If it is a variant Issue, title of the original Issue, else None.
        price: Price of the Issue.
        pull_count:
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
    date_foc: Annotated[Optional[date], BeforeValidator(ensure_date)] = None
    date_modified: datetime
    description: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    format: str
    id: int
    is_collected: Annotated[bool, Field(alias="collected"), BeforeValidator(ensure_bool)]
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(ensure_bool)]
    is_pulled: Annotated[bool, Field(alias="pulled"), BeforeValidator(ensure_bool)]
    is_read: Annotated[bool, Field(alias="readlist"), BeforeValidator(ensure_bool)]
    is_variant: Annotated[bool, Field(alias="variant"), BeforeValidator(ensure_bool)]
    is_wished: Annotated[bool, Field(alias="wishlist"), BeforeValidator(ensure_bool)]
    key_level: str
    my_pick: Optional[str] = None
    my_rating: Optional[str] = None
    my_rating_dec: Optional[str] = None
    parent_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    parent_title: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    price: Annotated[Optional[float], BeforeValidator(ensure_float)] = None
    publisher_id: int
    publisher_name: str
    pull_count: int = Field(alias="count_pulls")
    release_date: date = Field(alias="date_release")
    series_begin: int
    series_end: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    series_id: int
    series_name: str
    series_volume: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    title: str


class GenericCover(GenericComic):
    """The GenericCover object extends GenericIssue by including the type of cover used.

    Attributes:
        cover_type:
    """

    cover_type: int

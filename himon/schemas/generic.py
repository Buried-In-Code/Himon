"""The Generic module.

This module provides the following classes:

- ComicFormat
- CoverType
- GenericComic
- GenericCover
"""

__all__ = ["ComicFormat", "CoverType", "GenericComic", "GenericCover"]

from datetime import date, datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Annotated, Any

from pydantic import BeforeValidator, Field

from himon.schemas import BaseModel
from himon.schemas._validators import (
    validate_bool,
    validate_date,
    validate_decimal,
    validate_int,
    validate_str,
)


class ComicFormat(Enum):
    COMIC = "Comic"
    HARDCOVER = "Hardcover"
    TRADE_PAPERBACK = "Trade Paperback"


class GenericComic(BaseModel):
    """The GenericIssue object contains the base for related/link issues.

    Attributes:
        count_pulls:
        cover:
        date_foc: The date on the Front of Cover
        date_collected:
        date_modified: Date and time when the Issue was last updated.
        date_release: The date the Issue was released.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_enabled:
        is_variant: Issue has been marked as Variant.
        parent_id: If it is a variant Issue, id of the original Issue, else None.
        parent_title: If it is a variant Issue, title of the original Issue, else None.
        price: Price of the Issue.
        publisher_id: The publisher id of the Issue.
        publisher_name: The publisher name of the Issue.
        series_begin: The year the Series started.
        series_end: The year the Series ended.
        series_id: Identifier used by League of Comic Geeks.
        series_name: Name / Title of the Series.
        series_volume: Series volume number.
        title: Name/Title of the Issue.
    """

    count_pulls: int
    cover: int
    date_foc: Annotated[date | None, BeforeValidator(validate_date)] = None
    date_collected: Annotated[date | None, BeforeValidator(validate_date)] = None
    date_modified: datetime
    date_release: date
    description: Annotated[str | None, BeforeValidator(validate_str)] = None
    format: ComicFormat
    id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(validate_bool)]
    is_variant: Annotated[bool, Field(alias="variant"), BeforeValidator(validate_bool)]
    parent_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    parent_title: Annotated[str | None, BeforeValidator(validate_str)] = None
    price: Annotated[Decimal | None, BeforeValidator(validate_decimal)] = None
    publisher_id: int
    publisher_name: str
    series_begin: int
    series_end: Annotated[int | None, BeforeValidator(validate_int)] = None
    series_id: int
    series_name: str
    series_volume: Annotated[int | None, BeforeValidator(validate_int)] = None
    title: str

    def __init__(self, **data: Any):
        del_fields = (
            "collected",
            "pulled",
            "readlist",
            "wishlist",
            "key_level",
            "my_pick",
            "my_rating",
            "my_rating_dec",
        )
        for field in del_fields:
            del data[field]
        super().__init__(**data)


class CoverType(IntEnum):
    REPRINT = 1
    INCENTIVE = 2
    EVENT_EXCLUSIVE = 4


class GenericCover(GenericComic):
    """The GenericCover object extends GenericIssue by including the type of cover used.

    Attributes:
        cover_type:
    """

    cover_type: CoverType

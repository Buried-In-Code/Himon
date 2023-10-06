"""The Comic module.

This module provides the following classes:

- Comic
"""
__all__ = ["Comic"]
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Type

from pydantic import Field, field_validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_bool, to_optional_float, to_optional_int, to_optional_str
from himon.schemas.search_result import SearchResult
from himon.schemas.series import Series


class Variant(BaseModel):
    """The Variant object contains information for a variant comic.

    Attributes:
        date_modified: Date and time when the Variant was last updated.
        id: Identifier used by League of Comic Geeks.
        price: Price of the Variant.
        release_date: The date the Variant was released.
        title: Name/Title of the Variant.
    """

    date_modified: datetime
    id: int  # noqa: A003
    price: Optional[float] = None
    release_date: date = Field(alias="date_release")
    title: str

    @field_validator("price", mode="before")
    def _to_optional_float(cls: Type["Variant"], v: str) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)


class KeyEvent(BaseModel):
    """The KeyEvent object contains information for a key event.

    Attributes:
        character_id: Identifier used by League of Comic Geeks.
        id: Identifier used by League of Comic Geeks.
        name: Name/Title of the Event.
        note: Unknown field
        parent_name: Unknown field
        type: Unknown field
        type_id: Identifier used by League of Comic Geeks.
        universe_name: Universe this Event took place in.
    """

    character_id: int
    id: int  # noqa: A003
    name: str
    note: Optional[str] = None
    parent_name: Optional[str] = None
    type: int  # How is it different to type_id?  # noqa: A003
    type_id: int
    universe_name: str

    @field_validator("note", "parent_name", mode="before")
    def _to_optional_str(cls: Type["KeyEvent"], v: str) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class Creator(BaseModel):
    """The Creator object contains information for a creator.

    Attributes:
        id: Identifier used by League of Comic Geeks.
        name: Name/Title of the Creator.
        role: List of roles the Creator has in the comic. Separated by `,`.
        role_id: List of role ids the Creator has in the comic. Separated by `,`.
    """

    id: int  # noqa: A003
    name: str
    role: str
    role_id: str

    @property
    def roles(self: "Creator") -> Dict[int, str]:
        """Return a dict of role id and role name the Creator is attached to."""
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict


class Character(BaseModel):
    """The Character object contains information for a character.

    Attributes:
        date_added: Date and time when the Character was added.
        date_modified: Date and time when the Character was last updated.
        full_name: Full name of Character
        id: Identifier used by League of Comic Geeks.
        is_enabled: Unknown field
        name: Name/Alias of Character.
        parent_id: Unknown field
        parent_name: Unknown field
        publisher_name: The publisher name of Character.
        type_id: Unknown field
        universe_id: Universe id this Character is from.
        universe_name: Universe name this Character is from.
    """

    date_added: datetime
    date_modified: datetime
    full_name: str
    id: int  # noqa: A003
    is_enabled: bool = Field(alias="enabled")
    name: str
    parent_id: Optional[int] = None
    parent_name: Optional[str] = None
    publisher_name: str
    type_id: int
    universe_id: Optional[int] = None
    universe_name: Optional[str] = None

    @field_validator("parent_name", "universe_name", mode="before")
    def _to_optional_str(cls: Type["Character"], v: str) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @field_validator("parent_id", "universe_id", mode="before")
    def _to_optional_int(cls: Type["Character"], v: str) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("is_enabled", mode="before")
    def _to_bool(cls: Type["Character"], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)


class Comic(BaseModel):
    """The Comic object contains information for a comic.

    Attributes:
        characters: List of Characters in the Comic.
        collected_in: List of Comics this has been collected in.
        creators: List of Creators associated with the Comic
        date_added: Date and time when the Comic was added.
        date_modified: Date and time when the Comic was last updated.
        description: Description of the Comic.
        format: Type of Comic.
        id: Identifier used by League of Comic Geeks.
        is_enabled: Unknown field
        is_nsfw: Comic has been marked as NSFW
        is_variant: Comic has been marked as Variant
        isbn: ISBN identifier
        key_events: List of Key Events taken place in the Comic.
        page_count: Count of pages in the Comic.
        parent_id: If it is a variant comic, id of the original comic.
        parent_title: If it is a variant comic, title of the origin comic.
        price: Price of Comic
        release_date: The date the Comic was released.
        series: The series this Comic comes from.
        sku: SKU identifier.
        title: Name/Title of the Comic.
        upc: UPC identifier.
        variants: List of variants this Comic has.
    """

    characters: List[Character] = Field(default_factory=list)
    collected_in: List[SearchResult] = Field(default_factory=list)
    creators: List[Creator] = Field(default_factory=list)
    date_added: datetime
    date_modified: datetime
    description: Optional[str] = None
    format: str  # noqa: A003
    id: int  # noqa: A003
    is_enabled: bool = Field(alias="enabled")
    is_nsfw: bool = Field(alias="nsfw")
    is_variant: bool = Field(alias="variant")
    isbn: Optional[int] = None
    key_events: List[KeyEvent] = Field(default_factory=list)
    page_count: int = Field(alias="pages")
    parent_id: Optional[int] = None
    parent_title: Optional[str] = None
    price: Optional[float] = None
    release_date: date = Field(alias="date_release")
    series: Series
    sku: str
    title: str
    upc: Optional[int] = None
    variants: List[Variant] = Field(default_factory=list)

    def __init__(self: "Comic", **data: Any):
        if data["keys"]:
            data["key_events"] = list(data["keys"].values())
        for key, value in data["details"].items():
            data[key] = value
        super().__init__(**data)

    @field_validator("isbn", "parent_id", "upc", mode="before")
    def _to_optional_int(cls: Type["Comic"], v: str) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("is_enabled", "is_nsfw", "is_variant", mode="before")
    def _to_bool(cls: Type["Comic"], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("description", "parent_title", mode="before")
    def _to_optional_str(cls: Type["Comic"], v: str) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @field_validator("price", mode="before")
    def _to_optional_float(cls: Type["Comic"], v: str) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

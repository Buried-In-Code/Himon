"""
The Comic module.

This module provides the following classes:

- ComicModel
- Variant
- KeyEvent
- Creator
- Character
- Comic
"""
__all__ = ["Comic", "ComicModel", "Character", "Creator", "KeyEvent", "Variant"]
from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str
from himon.schemas.search_result import SearchResult
from himon.schemas.series import Series


class ComicModel(BaseModel):
    """Base model for Comic and subclasses."""

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore


class Variant(ComicModel):
    """The Variant object contains information for a variant comic."""

    date_modified: datetime  #: Date and time when the Variant was last updated.
    price: Optional[float] = None  #: Price of the Variant.
    release_date: date = Field(alias="date_release")  #: The date the Variant was released.
    title: str  #: Name/Title of the Variant.
    variant_id: int = Field(alias="id")  #: Identifier used in League of Comic Geeks.

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)


class KeyEvent(ComicModel):
    """The KeyEvent object contains information for a key event."""

    character_id: int  #: Identifier used in League of Comic Geeks.
    event_id: int = Field(alias="id")  #: Identifier used in League of Comic Geeks.
    name: str  #: Name/Title of the Comic.
    note: Optional[str] = None
    parent_name: Optional[str] = None  # TODO: Unknown field
    type: int  # TODO: How is it different to type_id?
    type_id: int  #: Identifier used in League of Comic Geeks.
    universe_name: str  #: Universe this key event took place in.

    @validator("note", "parent_name", pre=True)
    def validate_optional_str(cls, v):
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class Creator(ComicModel):
    """The Creator object contains information for a creator."""

    creator_id: int = Field(alias="id")  #: Identifier used in League of Comic Geeks.
    name: str  #: Name/Title of Creator
    role: str  #: Separated by ``,``.
    role_id: str  #: Separated by ``,``.

    @property
    def roles(self) -> Dict[int, str]:
        """Return a dict of role id and role name the Creator is attached to."""
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict


class Character(ComicModel):
    """The Character object contains information for a character."""

    character_id: int = Field(alias="id")  #: Identifier used by League of Comic Geeks.
    date_added: datetime  #: Date and time when the Character was added.
    date_modified: datetime  #: Date and time when the Character was last updated.
    full_name: str  #: Full name of Character
    is_enabled: bool = Field(alias="enabled")
    name: str  #: Name/Alias of Character
    parent_id: Optional[int] = None  # TODO: Unknown field
    parent_name: Optional[str] = None  # TODO: Unknown field
    publisher_name: str  #: The publisher name of Character.
    type_id: int
    universe_id: Optional[int] = None  #: Universe id this Character is from.
    universe_name: Optional[str] = None  #: Universe name this Character is from.

    @validator("parent_name", "universe_name", pre=True)
    def validate_optional_str(cls, v):
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("parent_id", "universe_id", pre=True)
    def validate_optional_int(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v):
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)


class Comic(ComicModel):
    """The Comic object contains information for a comic."""

    characters: List[Character] = Field(default_factory=list)  #: List of Characters in the Comic.
    collected_in: List[SearchResult] = Field(
        default_factory=list
    )  #: List of Comics this has been collected in.
    comic_id: int = Field(alias="id")  #: Identifier used by League of Comic Geeks.
    creators: List[Creator] = Field(
        default_factory=list
    )  #: List of Creators associated with the Comic.
    date_added: datetime  #: Date and time when the Comic was added.
    date_modified: datetime  #: Date and time when the Comic was last updated.
    description: Optional[str] = None  #: Description of the Comic.
    format: str  #: Type of Comic
    is_enabled: bool = Field(alias="enabled")
    is_nsfw: bool = Field(alias="nsfw")  #: Comic has been marked as NSFW
    is_variant: bool = Field(alias="variant")  #: Comic has been marked as Variant
    isbn: Optional[int] = None  #: ISBN identifier
    key_events: List[KeyEvent] = Field(
        default_factory=list
    )  #: List of Key Events taken place in the Comic.
    page_count: int = Field(alias="pages")  #: Count of pages in the Comic
    parent_id: Optional[int] = None  #: If it is a variant comic, Id of the original comic.
    parent_title: Optional[str] = None  #: If it is a variant comic, Title of the original comic.
    price: Optional[float] = None  #: Price of Comic
    release_date: date = Field(alias="date_release")  #: The date the Comic was released.
    series: Series  #: The series this Comic comes from
    sku: str  #: SKU identifier
    title: str  #: Name/Title of the Comic
    upc: Optional[int] = None  #: UPC identifier
    variants: List[Variant] = Field(default_factory=list)  #: List of variants this Comic has.

    def __init__(self, **data):
        if data["keys"]:
            data["key_events"] = list(data["keys"].values())
        for key, value in data["details"].items():
            data[key] = value
        super().__init__(**data)

    @validator("isbn", "parent_id", "upc", pre=True)
    def validate_optional_int(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_enabled", "is_nsfw", "is_variant", pre=True)
    def validate_bool(cls, v):
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v):
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

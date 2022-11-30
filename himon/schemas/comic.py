"""
The Comic module.

This module provides the following classes:

- Variant
- KeyEvent
- Creator
- Character
- Comic
"""
__all__ = ["Comic", "Character", "Creator", "KeyEvent", "Variant"]
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
    """
    The Variant object contains information for a variant comic.

    Attributes:
        date_modified: Date and time when the Variant was last updated.
        price: Price of the Variant.
        release_date: The date the Variant was released.
        title: Name/Title of the Variant.
        variant_id: Identifier used by League of Comic Geeks.
    """

    date_modified: datetime
    price: Optional[float] = None
    release_date: date = Field(alias="date_release")
    title: str
    variant_id: int = Field(alias="id")

    @validator("price", pre=True)
    def validate_optional_float(cls, v) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)


class KeyEvent(ComicModel):
    """
    The KeyEvent object contains information for a key event.

    Attributes:
        character_id: Identifier used by League of Comic Geeks.
        event_id: Identifier used by League of Comic Geeks.
        name: Name/Title of the Event.
        note:
        parent_name:
        type:
        type_id: Identifier used by League of Comic Geeks.
        universe_name: Universe this Event took place in.
    """

    character_id: int
    event_id: int = Field(alias="id")
    name: str
    note: Optional[str] = None
    parent_name: Optional[str] = None  # Unknown field
    type: int  # How is it different to type_id?
    type_id: int
    universe_name: Optional[str] = None

    @validator("note", "parent_name", pre=True)
    def validate_optional_str(cls, v) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class Creator(ComicModel):
    """
    The Creator object contains information for a creator.

    Attributes:
        creator_id: Identifier used by League of Comic Geeks.
        name: Name/Title of the Creator.
        role: List of roles the Creator has in the comic. Separated by `,`.
        role_id: List of role ids the Creator has in the comic. Separated by `,`.
    """

    creator_id: int = Field(alias="id")
    name: str
    role: str
    role_id: str

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
    """
    The Character object contains information for a character.

    Attributes:
        character_id: Identifier used by League of Comic Geeks.
        date_added: Date and time when the Character was added.
        date_modified: Date and time when the Character was last updated.
        full_name: Full name of Character
        is_enabled:
        name: Name/Alias of Character.
        parent_id:
        parent_name:
        publisher_name: The publisher name of Character.
        type_id:
        universe_id: Universe id this Character is from.
        universe_name: Universe name this Character is from.
    """

    character_id: int = Field(alias="id")
    date_added: datetime
    date_modified: datetime
    full_name: str
    is_enabled: bool = Field(alias="enabled")
    name: str
    parent_id: Optional[int] = None  # Unknown field
    parent_name: Optional[str] = None  # Unknown field
    publisher_name: Optional[str] = None
    type_id: int
    universe_id: Optional[int] = None
    universe_name: Optional[str] = None

    @validator("parent_name", "universe_name", pre=True)
    def validate_optional_str(cls, v) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("parent_id", "universe_id", pre=True)
    def validate_optional_int(cls, v) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)


class Comic(ComicModel):
    """
    The Comic object contains information for a comic.

    Attributes:
        characters: List of Characters in the Comic.
        collected_in: List of Comics this has been collected in.
        comic_id: Identifier used by League of Comic Geeks.
        creators: List of Creators associated with the Comic
        date_added: Date and time when the Comic was added.
        date_modified: Date and time when the Comic was last updated.
        description: Description of the Comic.
        format: Type of Comic.
        is_enabled:
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
    comic_id: int = Field(alias="id")
    creators: List[Creator] = Field(default_factory=list)
    date_added: datetime
    date_modified: datetime
    description: Optional[str] = None
    format: str
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

    def __init__(self, **data):
        if data["keys"]:
            data["key_events"] = list(data["keys"].values())
        for key, value in data["details"].items():
            data[key] = value
        super().__init__(**data)

    @validator("isbn", "parent_id", "upc", pre=True)
    def validate_optional_int(cls, v) -> Optional[int]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @validator("is_enabled", "is_nsfw", "is_variant", pre=True)
    def validate_bool(cls, v) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v) -> Optional[str]:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v) -> Optional[float]:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)

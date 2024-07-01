"""The Issue module.

This module provides the following classes:

- Comic
"""

from __future__ import annotations

__all__ = ["Comic"]
from datetime import date, datetime
from typing import Any

from pydantic import Field, HttpUrl, field_validator

from himon.schemas import BaseModel
from himon.schemas._validators import to_bool, to_optional_float, to_optional_int, to_optional_str
from himon.schemas.generic import GenericComic, GenericCover
from himon.schemas.series import Series


class Creator(BaseModel):
    """The Creator object contains information for a creator.

    Attributes:
        assoc_id:
        has_avatar: Creator has an avatar image.
        id: Identifier used by League of Comic Geeks.
        name: Name/Title of the Creator.
        role: List of roles the Creator has in the Issue. Separated by `,`.
        role_id: List of role ids the Creator has in the Issue. Separated by `,`.
        slug: The creator name slugged to be usable in a url.
        story_id:
    """

    assoc_id: int
    has_avatar: bool = Field(alias="avatar")
    id: int
    name: str
    role: str
    role_id: str
    slug: str
    story_id: int | None = None

    @property
    def roles(self: Creator) -> dict[int, str]:
        """Return a dict of role id and role name the Creator is attached to."""
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict

    @field_validator("has_avatar", mode="before")
    def _to_bool(cls: type[Creator], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("story_id", mode="before")
    def _to_optional_int(cls: type[Creator], v: str) -> int | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)


class Character(BaseModel):
    """The Character object contains information for a character.

    Attributes:
        avatar_id:
        banner:
        date_added: Date and time when the Character was added.
        date_modified: Date and time when the Character was last updated.
        full_name: Full name of Character.
        has_avatar: Character has an avatar image.
        id: Identifier used by League of Comic Geeks.
        map_to_id:
        name: Name/Alias of Character.
        parent_id:
        parent_name: The actual name/identity of the character.
        publisher_name: The publisher name of Character.
        story_id:
        type_id: 1 - Main, 2 - Supporting, 3 - Cameo
        universe_id: Universe id this Character is from.
        universe_name: Universe name this Character is from.
    """

    avatar_id: int | None = None
    banner: int
    date_added: datetime
    date_modified: datetime
    full_name: str
    has_avatar: bool = Field(alias="avatar")
    id: int
    map_to_id: int
    name: str
    parent_id: int | None = None
    parent_name: str | None = None
    publisher_name: str
    story_id: int
    type_id: int
    universe_id: int | None = None
    universe_name: str | None = None

    @field_validator("has_avatar", mode="before")
    def _to_bool(cls: type[Character], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("parent_id", "universe_id", "avatar_id", mode="before")
    def _to_optional_int(cls: type[Character], v: str) -> int | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_int(v)

    @field_validator("parent_name", "universe_name", mode="before")
    def _to_optional_str(cls: type[Character], v: str) -> str | None:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class KeyEvent(BaseModel):
    """The KeyEvent object contains information for a key events such as Key Appearances.

    Attributes:
        character_id: Identifier used by League of Comic Geeks.
        comic_id: Issue id this event is attached to.
        id: Identifier used by League of Comic Geeks.
        name: Superhero name/alias.
        note: Duplicate of 'string_secondary'.
        parent_name: The actual name/identity of the character.
        string_description: Full name of Character.
        string_primary: Text version of the type of event.
        string_secondary:
        type: 1 - First Appearance, 2 - Death
        type_id: Identifier used by League of Comic Geeks.
        universe_name: Universe this Event took place in.
    """

    character_id: int
    comic_id: int
    id: int
    name: str
    note: str | None = None
    parent_name: str | None = None
    string_description: str
    string_primary: str
    string_secondary: str | None = None
    type: int
    type_id: int
    universe_name: str

    @field_validator("note", "parent_name", "string_secondary", mode="before")
    def _to_optional_str(cls: type[KeyEvent], v: str) -> str | None:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)


class Variant(BaseModel):
    """The Variant object contains information for a variant Issue.

    Attributes:
        cover:
        cover_type: 1 - Reprint, 2 - Incentive, 3 - , 4 - Event Exclusive
        date_foc:
        date_modified: Date and time when the Variant was last updated.
        id: Identifier used by League of Comic Geeks.
        price: Price of the Variant.
        release_date: The date the Variant was released.
        sku: SKU identifier.
        title: Name/Title of the Variant.
    """

    cover: int
    cover_type: int
    date_foc: date | None = None
    date_modified: datetime
    id: int
    price: float | None = None
    release_date: date = Field(alias="date_release")
    sku: str
    title: str

    @field_validator("date_foc", mode="before")
    def _to_optional_date(cls: type[Variant], v: str) -> date | None:
        """Pydantic validator to convert a Str or 0 to None or return date."""
        return to_optional_float(v)

    @field_validator("price", mode="before")
    def _to_optional_float(cls: type[Variant], v: str) -> float | None:
        """Pydantic validator to convert a Str or 0 to None or return value."""
        return to_optional_float(v)


class Comic(BaseModel):
    """The Issue object contains information for an Issue.

    Attributes:
        banner:
        characters: List of Characters in the Issue.
        collected_in: List of Issues this has been collected in.
        collected_issues: List of Issues this has collected.
        covers: List of Covers associated with the Issue.
        creators: List of Creators associated with the Issue
        keys: List of Key Events taken place in the Issue.
        series: The series this Issue comes from.
        variants: List of variants this Issue has.
        cover:
        date_added: Date and time when the Issue was added.
        date_cover:
        date_foc:
        date_modified: Date and time when the Issue was last updated.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_nsfw: Issue has been marked as NSFW.
        is_variant: Issue has been marked as Variant.
        isbn: ISBN identifier
        page_count: Count of pages in the Issue.
        parent_id: If it is a variant Issue, id of the original Issue.
        parent_title: If it is a variant Issue, title of the original Issue.
        price: Price of the Issue.
        publisher_id: The publisher id of the Issue.
        publisher_name: The publisher name of the Issue.
        publisher_slug: The publisher name slugged to be usable in a url.
        release_date: The date the Issue was released.
        series_id: The series id of the Issue.
        sku: SKU identifier.
        title: Name/Title of the Issue.
        upc: UPC identifier.
    """

    banner: HttpUrl
    characters: list[Character] = Field(default_factory=list)
    collected_in: list[GenericComic] = Field(default_factory=list)
    collected_issues: list[GenericComic] = Field(default_factory=list)
    covers: list[GenericCover] = Field(default_factory=list)
    creators: list[Creator] = Field(default_factory=list)
    keys: list[KeyEvent] = Field(default_factory=list)
    series: Series
    variants: list[Variant] = Field(default_factory=list)
    cover: int
    date_added: datetime
    date_cover: date | None = None
    date_foc: date | None = None
    date_modified: datetime
    description: str | None = None
    format: str
    id: int
    is_nsfw: bool = Field(alias="nsfw")
    is_variant: bool = Field(alias="variant")
    isbn: int | None = None
    page_count: int = Field(alias="pages")
    parent_id: int | None = None
    parent_title: str | None = None
    price: float | None = None
    publisher_id: int
    publisher_name: str
    publisher_slug: str
    release_date: date = Field(alias="date_release")
    series_id: int
    sku: str
    title: str
    upc: int | None = None

    def __init__(self: Comic, **data: Any):
        for key, value in data["details"].items():
            data[key] = value
        del data["details"]
        super().__init__(**data)

    @field_validator("is_nsfw", "is_variant", mode="before")
    def _to_bool(cls: type[Comic], v: str) -> bool:
        """Pydantic validator to convert a Str 0/1 to a bool."""
        return to_bool(v)

    @field_validator("date_cover", "date_foc", mode="before")
    def _to_optional_date(cls: type[Comic], v: str) -> date | None:
        """Pydantic validator to convert a Str or 0 to None or return date."""
        return to_optional_float(v)

    @field_validator("price", mode="before")
    def _to_optional_float(cls: type[Comic], v: str) -> float | None:
        """Pydantic validator to convert a Str or 0 to None or return float."""
        return to_optional_float(v)

    @field_validator("isbn", "parent_id", "upc", mode="before")
    def _to_optional_int(cls: type[Comic], v: str) -> int | None:
        """Pydantic validator to convert a Str or 0 to None or return int."""
        return to_optional_int(v)

    @field_validator("description", "parent_title", mode="before")
    def _to_optional_str(cls: type[Comic], v: str) -> str | None:
        """Pydantic validator to convert a Str to None or return html stripped value."""
        return to_optional_str(v)

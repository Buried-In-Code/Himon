"""The Issue module.

This module provides the following classes:

- CharacterType
- Comic
- KeyEventType
"""

__all__ = ["CharacterType", "Comic", "KeyEventType"]

from datetime import date, datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Annotated, Any

from pydantic import BeforeValidator, Field, HttpUrl

from himon.schemas import BaseModel
from himon.schemas._validators import (
    validate_bool,
    validate_date,
    validate_decimal,
    validate_int,
    validate_str,
)
from himon.schemas.generic import ComicFormat, CoverType, GenericComic, GenericCover
from himon.schemas.series import Series


class CharacterType(Enum):
    MAIN = "1"
    SUPPORTING = "2"
    CAMEO = "3"


class Character(BaseModel):
    """The Character object contains information for a character.

    Attributes:
        avatar_comic_id:
        avatar_id:
        banner:
        character_type:
        continuity_id:
        current_persona:
        date_added: Date and time when the Character was added.
        date_modified: Date and time when the Character was last updated.
        full_name: Full name of Character.
        has_avatar: Character has an avatar image.
        id: Identifier used by League of Comic Geeks.
        individual_id:
        is_enabled:
        map_to_id:
        name: Name/Alias of Character.
        parent_id:
        parent_name: The actual name/identity of the character.
        publisher_name: The publisher name of Character.
        role_name:
        role_note:
        slug:
        story_id:
        tier_id:
        universe_id: Universe id this Character is from.
        universe_name: Universe name this Character is from.
    """

    avatar_comic_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    avatar_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    banner: int
    character_type: Annotated[CharacterType, Field(alias="type_id")]
    continuity_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    current_persona: Annotated[int | None, BeforeValidator(validate_int)] = None
    date_added: datetime
    date_modified: datetime
    full_name: str
    has_avatar: Annotated[bool, Field(alias="avatar"), BeforeValidator(validate_bool)]
    id: int
    individual_id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(validate_bool)]
    map_to_id: int
    name: str
    parent_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    parent_name: Annotated[str | None, BeforeValidator(validate_str)] = None
    publisher_name: str
    role_name: str
    role_note: Annotated[str | None, BeforeValidator(validate_str)] = None
    slug: Annotated[str | None, BeforeValidator(validate_str)] = None
    story_id: int
    tier_id: int
    universe_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    universe_name: Annotated[str | None, BeforeValidator(validate_str)] = None


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
    has_avatar: Annotated[bool, Field(alias="avatar"), BeforeValidator(validate_bool)]
    id: int
    name: str
    role: str
    role_id: str
    slug: str
    story_id: Annotated[int | None, BeforeValidator(validate_int)] = None

    @property
    def roles(self) -> dict[int, str]:
        """Return a dict of role id and role name the Creator is attached to."""
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict


class KeyEventType(IntEnum):
    FIRST_APPEARANCE = 1
    DEATH = 2


class KeyEvent(BaseModel):
    """The KeyEvent object contains information for a key events such as Key Appearances.

    Attributes:
        character_id: Identifier used by League of Comic Geeks.
        comic_id: Issue id this event is attached to.
        id: Identifier used by League of Comic Geeks.
        key_event_type:
        name: Superhero name/alias.
        note: Duplicate of 'string_secondary'.
        parent_name: The actual name/identity of the character.
        string_description: Full name of Character.
        string_primary: Text version of the type of event.
        string_secondary:
        type_id: Identifier used by League of Comic Geeks.
        universe_id:
        universe_name: Universe this Event took place in.
    """

    character_id: int
    comic_id: int
    id: int
    key_event_type: Annotated[KeyEventType, Field(alias="type")]
    name: str
    note: Annotated[str | None, BeforeValidator(validate_str)] = None
    parent_name: Annotated[str | None, BeforeValidator(validate_str)] = None
    string_description: str
    string_primary: str
    string_secondary: Annotated[str | None, BeforeValidator(validate_str)] = None
    type_id: int
    universe_id: int
    universe_name: str


class Variant(BaseModel):
    """The Variant object contains information for a variant Issue.

    Attributes:
        cover:
        cover_type:
        date_foc:
        date_modified: Date and time when the Variant was last updated.
        date_release: The date the Variant was released.
        id: Identifier used by League of Comic Geeks.
        price: Price of the Variant.
        sku: SKU identifier.
        title: Name/Title of the Variant.
    """

    cover: int
    cover_type: CoverType
    date_foc: Annotated[date | None, BeforeValidator(validate_date)] = None
    date_modified: datetime
    date_release: date
    id: int
    price: Annotated[Decimal | None, BeforeValidator(validate_decimal)] = None
    sku: str
    title: str


class Comic(BaseModel):
    """The Issue object contains information for an Issue.

    Attributes:
        banner:
        characters: List of Characters in the Issue.
        collected_in: List of Issues this has been collected in.
        collected_issues: List of Issues this has collected.
        consensus_users:
        count_collected:
        count_pulls:
        count_read:
        count_votes:
        cover:
        covers: List of Covers associated with the Issue.
        creators: List of Creators associated with the Issue
        date_added: Date and time when the Issue was added.
        date_cover:
        date_foc:
        date_modified: Date and time when the Issue was last updated.
        date_release: The date the Issue was released.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_enabled:
        is_nsfw: Issue has been marked as NSFW.
        is_variant: Issue has been marked as Variant.
        isbn: ISBN identifier
        keys: List of Key Events taken place in the Issue.
        pages: Count of pages in the Issue.
        parent_id: If it is a variant Issue, id of the original Issue.
        parent_title: If it is a variant Issue, title of the original Issue.
        price: Price of the Issue.
        publisher_id: The publisher id of the Issue.
        publisher_name: The publisher name of the Issue.
        publisher_slug: The publisher name slugged to be usable in a url.
        series: The series this Issue comes from.
        series_id: The series id of the Issue.
        sku: SKU identifier.
        sku_diamond:
        sku_lunar:
        title: Name/Title of the Issue.
        upc: UPC identifier.
        variants: List of variants this Issue has.
    """

    banner: HttpUrl
    characters: list[Character] = Field(default_factory=list)
    collected_in: list[GenericComic] = Field(default_factory=list)
    collected_issues: list[GenericComic] = Field(default_factory=list)
    consensus_users: Decimal
    count_collected: int
    count_pulls: int
    count_read: int
    count_votes: int
    cover: int
    covers: list[GenericCover] = Field(default_factory=list)
    creators: list[Creator] = Field(default_factory=list)
    date_added: datetime
    date_cover: Annotated[date | None, BeforeValidator(validate_date)] = None
    date_foc: Annotated[date | None, BeforeValidator(validate_date)] = None
    date_modified: datetime
    date_release: date
    description: Annotated[str | None, BeforeValidator(validate_str)] = None
    format: ComicFormat
    id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(validate_bool)]
    is_nsfw: Annotated[bool, Field(alias="nsfw"), BeforeValidator(validate_bool)]
    is_variant: Annotated[bool, Field(alias="variant"), BeforeValidator(validate_bool)]
    isbn: Annotated[int | None, BeforeValidator(validate_int)] = None
    keys: list[KeyEvent] = Field(default_factory=list)
    pages: int
    parent_id: Annotated[int | None, BeforeValidator(validate_int)] = None
    parent_title: Annotated[str | None, BeforeValidator(validate_str)] = None
    price: Annotated[Decimal | None, BeforeValidator(validate_decimal)] = None
    publisher_id: int
    publisher_name: str
    publisher_slug: str
    series: Series
    series_id: int
    sku: str
    sku_diamond: str
    sku_lunar: Annotated[str | None, BeforeValidator(validate_str)] = None
    title: str
    upc: Annotated[int | None, BeforeValidator(validate_int)] = None
    variants: list[Variant] = Field(default_factory=list)

    def __init__(self, **data: Any):
        for key, value in data["details"].items():
            data[key] = value  # noqa: PERF403
        del_fields = (
            "details",
            "community_reviews",
            "comments",
            "key_text",
            "key_text_safe",
            "user_rating_count",
            "user_rating_likes",
            "user_review_count",
            "user_review_score",
            "user_review_avg",
            "user_rating_grade",
            "user_rating_color",
            "listed_members_count",
        )
        for field in del_fields:
            del data[field]
        super().__init__(**data)

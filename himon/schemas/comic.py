"""The Issue module.

This module provides the following classes:

- Comic
"""

__all__ = ["Comic"]

from datetime import date, datetime
from typing import Annotated, Any, Optional

from pydantic import BeforeValidator, Field, HttpUrl

from himon.schemas import BaseModel
from himon.schemas._validators import ensure_bool, ensure_date, ensure_float, ensure_int, ensure_str
from himon.schemas.generic import GenericComic, GenericCover
from himon.schemas.series import Series


class Character(BaseModel):
    """The Character object contains information for a character.

    Attributes:
        avatar_id:
        banner:
        current_persona:
        date_added: Date and time when the Character was added.
        date_modified: Date and time when the Character was last updated.
        full_name: Full name of Character.
        has_avatar: Character has an avatar image.
        id: Identifier used by League of Comic Geeks.
        is_enabled:
        map_to_id:
        name: Name/Alias of Character.
        parent_id:
        parent_name: The actual name/identity of the character.
        publisher_name: The publisher name of Character.
        role_name:
        role_note:
        story_id:
        type_id: 1 - Main, 2 - Supporting, 3 - Cameo
        universe_id: Universe id this Character is from.
        universe_name: Universe name this Character is from.
    """

    avatar_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    banner: int
    current_persona: str
    date_added: datetime
    date_modified: datetime
    full_name: str
    has_avatar: Annotated[bool, Field(alias="avatar"), BeforeValidator(ensure_bool)]
    id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(ensure_bool)]
    map_to_id: int
    name: str
    parent_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    parent_name: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    publisher_name: str
    role_name: str
    role_note: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    story_id: int
    type_id: int
    universe_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    universe_name: Annotated[Optional[str], BeforeValidator(ensure_str)] = None


class FeedData(BaseModel):
    count: Optional[int] = None
    debug: Optional[int] = None
    form_share: int
    list_: list = Field(alias="list", default_factory=list)
    name: str


class CommunityReview(BaseModel):
    count: Optional[int] = None
    debug: Optional[int] = None
    feed_data: FeedData
    list_: list = Field(alias="list", default_factory=list)


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
    has_avatar: Annotated[bool, Field(alias="avatar"), BeforeValidator(ensure_bool)]
    id: int
    name: str
    role: str
    role_id: str
    slug: str
    story_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None

    @property
    def roles(self) -> dict[int, str]:
        """Return a dict of role id and role name the Creator is attached to."""
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict


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
        universe_id:
        universe_name: Universe this Event took place in.
    """

    character_id: int
    comic_id: int
    id: int
    name: str
    note: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    parent_name: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    string_description: str
    string_primary: str
    string_secondary: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    type: int
    type_id: int
    universe_id: int
    universe_name: str


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
    date_foc: Annotated[Optional[date], BeforeValidator(ensure_date)] = None
    date_modified: datetime
    id: int
    price: Annotated[Optional[float], BeforeValidator(ensure_float)] = None
    release_date: date = Field(alias="date_release")
    sku: str
    title: str


class Comic(BaseModel):
    """The Issue object contains information for an Issue.

    Attributes:
        banner:
        characters: List of Characters in the Issue.
        collected_count:
        collected_in: List of Issues this has been collected in.
        collected_issues: List of Issues this has collected.
        comments:
        community_reviews:
        cover:
        covers: List of Covers associated with the Issue.
        creators: List of Creators associated with the Issue
        date_added: Date and time when the Issue was added.
        date_cover:
        date_foc:
        date_modified: Date and time when the Issue was last updated.
        description: Description of the Issue.
        format: Type of Issue.
        id: Identifier used by League of Comic Geeks.
        is_enabled:
        is_nsfw: Issue has been marked as NSFW.
        is_variant: Issue has been marked as Variant.
        isbn: ISBN identifier
        key_text:
        key_text_safe:
        keys: List of Key Events taken place in the Issue.
        listed_members_count:
        page_count: Count of pages in the Issue.
        parent_id: If it is a variant Issue, id of the original Issue.
        parent_title: If it is a variant Issue, title of the original Issue.
        price: Price of the Issue.
        publisher_id: The publisher id of the Issue.
        publisher_name: The publisher name of the Issue.
        publisher_slug: The publisher name slugged to be usable in a url.
        pull_count:
        read_count:
        release_date: The date the Issue was released.
        series: The series this Issue comes from.
        series_id: The series id of the Issue.
        sku: SKU identifier.
        sku_diamond:
        sku_lunar:
        title: Name/Title of the Issue.
        upc: UPC identifier.
        user_rating_color:
        user_rating_count:
        user_rating_grade:
        user_rating_likes:
        user_review_avg:
        user_review_count:
        user_review_score:
        variants: List of variants this Issue has.
        vote_count:
    """

    banner: HttpUrl
    characters: list[Character] = Field(default_factory=list)
    collected_count: Annotated[
        Optional[int], Field(alias="count_collected"), BeforeValidator(ensure_int)
    ] = None
    collected_in: list[GenericComic] = Field(default_factory=list)
    collected_issues: list[GenericComic] = Field(default_factory=list)
    comments: list[str] = Field(default_factory=list)
    community_reviews: CommunityReview
    consensus_users: float
    cover: int
    covers: list[GenericCover] = Field(default_factory=list)
    creators: list[Creator] = Field(default_factory=list)
    date_added: datetime
    date_cover: Annotated[Optional[date], BeforeValidator(ensure_date)] = None
    date_foc: Annotated[Optional[date], BeforeValidator(ensure_date)] = None
    date_modified: datetime
    description: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    format: str
    id: int
    is_enabled: Annotated[bool, Field(alias="enabled"), BeforeValidator(ensure_bool)]
    is_nsfw: Annotated[bool, Field(alias="nsfw"), BeforeValidator(ensure_bool)]
    is_variant: Annotated[bool, Field(alias="variant"), BeforeValidator(ensure_bool)]
    isbn: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    key_text: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    key_text_safe: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    keys: list[KeyEvent] = Field(default_factory=list)
    listed_members_count: int
    page_count: int = Field(alias="pages")
    parent_id: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    parent_title: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    price: Annotated[Optional[float], BeforeValidator(ensure_float)] = None
    publisher_id: int
    publisher_name: str
    publisher_slug: str
    pull_count: Annotated[
        Optional[int], Field(alias="count_pulls"), BeforeValidator(ensure_int)
    ] = None
    read_count: int = Field(alias="count_read")
    release_date: date = Field(alias="date_release")
    series: Series
    series_id: int
    sku: str
    sku_diamond: str
    sku_lunar: Annotated[Optional[str], BeforeValidator(ensure_str)] = None
    title: str
    upc: Annotated[Optional[int], BeforeValidator(ensure_int)] = None
    user_rating_color: str
    user_rating_count: int
    user_rating_grade: str
    user_rating_likes: int
    user_review_avg: Annotated[Optional[float], BeforeValidator(ensure_float)] = None
    user_review_count: int
    user_review_score: Annotated[Optional[float], BeforeValidator(ensure_float)] = None
    variants: list[Variant] = Field(default_factory=list)
    vote_count: Annotated[
        Optional[int], Field(alias="count_votes"), BeforeValidator(ensure_int)
    ] = None

    def __init__(self, **data: Any):
        for key, value in data["details"].items():
            data[key] = value  # noqa: PERF403
        del data["details"]
        super().__init__(**data)

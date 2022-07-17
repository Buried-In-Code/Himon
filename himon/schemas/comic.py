from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str
from himon.schemas.search_result import SearchResult
from himon.schemas.series import Series


class ComicModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore


class Variant(ComicModel):
    date_modified: datetime
    price: Optional[float] = None
    release_date: date = Field(alias="date_release")
    title: str
    variant_id: int = Field(alias="id")

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        return to_optional_float(v)


class KeyEvent(ComicModel):
    character_id: int
    event_id: int = Field(alias="id")
    name: str
    note: Optional[str] = None
    parent_name: Optional[str] = None  # Unknown
    type: int  # How is it different to type_id?
    type_id: int
    universe_name: str

    @validator("note", "parent_name", pre=True)
    def validate_optional_str(cls, v):
        return to_optional_str(v)


class Creator(ComicModel):
    creator_id: int = Field(alias="id")
    name: str
    role: str
    role_id: str

    @property
    def roles(self) -> Dict[int, str]:
        role_dict = {}
        id_list = self.role_id.split(",")
        role_list = self.role.split(",")
        for index, role_id in enumerate(id_list):
            role_dict[int(role_id)] = role_list[index].strip().title()
        return role_dict


class Character(ComicModel):
    character_id: int = Field(alias="id")
    date_added: datetime
    date_modified: datetime
    full_name: str
    is_enabled: bool = Field(alias="enabled")
    name: str
    parent_id: Optional[int] = None  # Unkmown
    parent_name: Optional[str] = None  # Unknown
    publisher_name: str
    type_id: int
    universe_id: Optional[int] = None
    universe_name: Optional[str] = None

    @validator("parent_name", "universe_name", pre=True)
    def validate_optional_str(cls, v):
        return to_optional_str(v)

    @validator("parent_id", "universe_id", pre=True)
    def validate_optional_int(cls, v):
        return to_optional_int(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v):
        return to_bool(v)


class Comic(ComicModel):
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
    parent_id: Optional[int] = None  #: Id of comic that this is a variant of.
    parent_title: Optional[str] = None  #: Title of comic that this is a variant of.
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
    def validate_optional_int(cls, v):
        return to_optional_int(v)

    @validator("is_enabled", "is_nsfw", "is_variant", pre=True)
    def validate_bool(cls, v):
        return to_bool(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v):
        return to_optional_str(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        return to_optional_float(v)

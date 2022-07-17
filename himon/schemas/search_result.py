from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str


class SearchResult(BaseModel):
    comic_id: int = Field(alias="id")
    date_modified: datetime
    description: Optional[str] = None
    format: str
    is_enabled: bool = Field(alias="enabled")
    is_variant: bool = Field(alias="variant")
    parent_id: Optional[int] = None  #: Id of comic that this is a variant of.
    parent_title: Optional[str] = None  #: Title of comic that this is a variant of.
    price: Optional[float] = None
    publisher_id: int
    publisher_name: str
    release_date: date = Field(alias="date_release")
    series_id: int
    series_name: str
    series_volume: Optional[int] = None
    title: str
    year_begin: int = Field(alias="series_begin")
    year_end: Optional[int] = Field(alias="series_end", default=None)

    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("parent_id", "series_volume", "year_end", pre=True)
    def validate_optional_int(cls, v):
        return to_optional_int(v)

    @validator("is_variant", "is_enabled", pre=True)
    def validate_bool(cls, v):
        return to_bool(v)

    @validator("price", pre=True)
    def validate_optional_float(cls, v):
        return to_optional_float(v)

    @validator("description", "parent_title", pre=True)
    def validate_optional_str(cls, v):
        return to_optional_str(v)

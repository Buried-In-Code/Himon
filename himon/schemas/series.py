from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from himon.schemas import to_bool, to_optional_int, to_optional_str


class Series(BaseModel):
    date_added: datetime
    date_modified: datetime
    description: Optional[str] = None
    is_enabled: bool = Field(alias="enabled")
    publisher_id: int
    publisher_name: str
    series_id: int = Field(alias="id")
    title: str
    volume: Optional[int] = None
    year_begin: int
    year_end: Optional[int] = None

    class Config:
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

    @validator("description", pre=True)
    def validate_optional_str(cls, v):
        return to_optional_str(v)

    @validator("is_enabled", pre=True)
    def validate_bool(cls, v):
        return to_bool(v)

    @validator("volume", "year_end", pre=True)
    def validate_optional_int(cls, v):
        return to_optional_int(v)

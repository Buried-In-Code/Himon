"""himon.schemas package entry file."""
__all__ = ["BaseModel"]

from pydantic import BaseModel as PydanticModel, Extra


class BaseModel(PydanticModel):
    """Base model for himon resources."""

    class Config:
        """Any extra fields will be ignored, strings will have start/end whitespace stripped."""

        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        extra = Extra.ignore

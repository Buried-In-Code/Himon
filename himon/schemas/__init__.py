"""himon.schemas package entry file.

This module provides the following classes:

- BaseModel
"""

__all__ = ["BaseModel"]

from pydantic import BaseModel as PydanticModel


class BaseModel(
    PydanticModel,
    populate_by_name=True,
    str_strip_whitespace=True,
    validate_assignment=True,
    revalidate_instances="always",
    extra="forbid",
):
    """Base model for himon resources."""

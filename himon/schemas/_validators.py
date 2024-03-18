from __future__ import annotations

__all__ = ["to_optional_str", "to_optional_int", "to_optional_float", "to_bool"]

import html
import re
from datetime import date, datetime


def to_optional_date(v: str) -> date | None:
    """Convert a Str or 0 to None or return date.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or date
    """
    if not v or v == "0000-00-00":
        return None
    try:
        return datetime.strptime(v, "%y-%m-%d").date()  # noqa: DTZ007
    except ValueError:
        return None


def to_optional_int(v: str) -> int | None:
    """Convert a Str or 0 to None or return int.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or int
    """
    try:
        if not v or int(v) == 0:
            return None
        return int(v)
    except ValueError:
        return None


def to_optional_float(v: str) -> float | None:
    """Convert a Str or 0 to None or return float.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or float
    """
    if v:
        v = str(v).replace("..", ".")
    try:
        if not v or float(v) == 0:
            return None
        return float(v)
    except ValueError:
        return None


def to_bool(v: str) -> bool:
    """Convert a Str 0/1 to a bool.

    Args:
        v: Value to convert
    Return:
        Value mapped as Bool
    Raises:
        ValueError: If value isn't a 0/1
    """
    if str(v) == "0":
        return False
    if str(v) == "1":
        return True
    msg = f"Unknown bool value `{v}`."
    raise ValueError(msg)


def to_optional_str(v: str) -> str | None:
    """Convert a Str to None or return html stripped value.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or html stripped value
    """
    if not v:
        return None
    regex = re.compile(r"(<!--.*?-->|<[^>]*>)")
    output = " ".join(html.unescape(regex.sub("", v.strip())).split())
    return output if output else None

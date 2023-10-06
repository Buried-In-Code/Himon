__all__ = ["to_optional_str", "to_optional_int", "to_optional_float", "to_bool"]

import html
import re
from typing import Optional


def to_optional_int(v: str) -> Optional[int]:
    """Convert a Str or 0 to None or return value.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or value
    """
    try:
        if not v or int(v) == 0:
            return None
        return int(v)
    except ValueError:
        return None


def to_optional_float(v: str) -> Optional[float]:
    """Convert a Str or 0 to None or return value.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or value
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


def to_optional_str(v: str) -> Optional[str]:
    """Convert a Str to None or return html stripped value.

    Args:
        v: Value to convert
    Return:
        Value mapped as None or html stripped value
    """
    if not v:
        return None
    regex = re.compile(r"(<!--.*?-->|<[^>]*>)")
    return " ".join(html.unescape(regex.sub("", v.strip())).split())

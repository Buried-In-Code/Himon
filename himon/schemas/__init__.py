__all__ = ["to_optional_str", "to_optional_int", "to_optional_float", "to_bool"]

import html
import re
from typing import Optional


def to_optional_int(v) -> Optional[int]:
    if not v or int(v) == 0:
        return None
    return v


def to_optional_float(v) -> Optional[float]:
    if v:
        v = str(v).replace("..", ".")
    if not v or float(v) == 0:
        return None
    return v


def to_bool(v) -> bool:
    if str(v) == "0":
        return False
    if str(v) == "1":
        return True
    raise ValueError(f"Unknown bool value `{v}`.")


def to_optional_str(v) -> Optional[str]:
    if not v:
        return None
    regex = re.compile(r"(<!--.*?-->|<[^>]*>)")
    return " ".join(html.unescape(regex.sub("", v.strip())).split())

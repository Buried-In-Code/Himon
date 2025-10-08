__all__ = ["validate_bool", "validate_date", "validate_decimal", "validate_int", "validate_str"]

import html
import re
from datetime import date, datetime
from decimal import Decimal


def validate_bool(value: str) -> bool:
    """Convert a Str 0/1 to a bool.

    Args:
        value: Value to convert
    Return:
        Value mapped as Bool
    Raises:
        ValueError: If value isn't a 0/1
    """
    if str(value) == "0":
        return False
    if str(value) == "1":
        return True
    raise ValueError("Unknown bool value `%s`.", value)


def validate_date(value: str) -> date | None:
    """Convert a Str or 0 to None or return date.

    Args:
        value: Value to convert
    Return:
        Value mapped as None or date
    """
    if not value or value == "0000-00-00":
        return None
    try:
        return datetime.strptime(value, "%y-%m-%d").date()  # noqa: DTZ007
    except ValueError:
        return None


def validate_decimal(value: str) -> Decimal | None:
    """Convert a Str or 0 to None or return Decimal.

    Args:
        value: Value to convert
    Return:
        Value mapped as None or Decimal
    """
    if value:
        value = str(value).replace("..", ".")
    try:
        if not value or float(value) == 0:
            return None
        return Decimal(value)
    except ValueError:
        return None


def validate_int(value: str) -> int | None:
    """Convert a Str or 0 to None or return int.

    Args:
        value: Value to convert
    Return:
        Value mapped as None or int
    """
    try:
        if not value or int(value) == 0:
            return None
        return int(value)
    except ValueError:
        return None


def validate_str(value: str) -> str | None:
    """Convert a Str to None or return html stripped value.

    Args:
        value: Value to convert
    Return:
        Value mapped as None or html stripped value
    """
    if not value:
        return None
    regex = re.compile(r"(<!--.*?-->|<[^>]*>)")
    output = " ".join(html.unescape(regex.sub("", value.strip())).split())
    return output if output else None

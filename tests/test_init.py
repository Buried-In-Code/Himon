"""
The init test module.

This module contains tests for himon.schemas.__init__ functions.
"""
import pytest

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str


def test_optional_int():
    """Test converting an Int to an Optional[Int]."""
    output = to_optional_int(12)
    assert output == 12


def test_optional_int_str():
    """Test converting a Str to an Optional[Int]."""
    output = to_optional_int("12")
    assert output == "12"


def test_optional_int_invalid():
    """Test converting an invalid value to an Optional[Int]."""
    with pytest.raises(ValueError):
        to_optional_int("Not Integer")


def test_optional_int_zero():
    """Test converting a 0 to an Optional[Int]."""
    output = to_optional_int("0")
    assert output is None


def test_optional_int_none():
    """Test converting a None to an Optional[Int]."""
    output = to_optional_int(None)
    assert output is None


def test_optional_float():
    """Test converting a Float to an Optional[Float]."""
    output = to_optional_float(1.23)
    assert output == "1.23"


def test_optional_float_str():
    """Test converting a Str to an Optional[Float]."""
    output = to_optional_float("1.23")
    assert output == "1.23"


def test_optional_float_double_decimal():
    """Test converting a Str with a double decimal to an Optional[Float]."""
    output = to_optional_float("1..23")
    assert output == "1.23"


def test_optional_float_invalid():
    """Test converting an invalid value to an Optional[Float]."""
    with pytest.raises(ValueError):
        to_optional_float("Not Float")


def test_optional_float_zero():
    """Test converting a 0 to an Optional[Float]."""
    output = to_optional_float("0")
    assert output is None


def test_optional_float_none():
    """Test converting a None to an Optional[Float]."""
    output = to_optional_float(None)
    assert output is None


def test_optional_str():
    """Test converting a Str to an Optional[Str]."""
    output = to_optional_str("String value")
    assert output == "String value"


def test_optional_str_none():
    """Test converting a None to an Optional[Str]."""
    output = to_optional_str(None)
    assert output is None


def test_bool_true():
    """Test converting a Str to a Bool."""
    output = to_bool("1")
    assert output is True


def test_bool_false():
    """Test converting a Str to a Bool."""
    output = to_bool("0")
    assert output is False


def test_bool_invalid():
    """Test converting an invalid value to a Bool."""
    with pytest.raises(ValueError):
        to_bool("2")

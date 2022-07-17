import pytest

from himon.schemas import to_bool, to_optional_float, to_optional_int, to_optional_str


def test_optional_int():
    output = to_optional_int(12)
    assert output == 12


def test_optional_int_str():
    output = to_optional_int("12")
    assert output == "12"


def test_optional_int_invalid():
    with pytest.raises(ValueError):
        to_optional_int("Not Integer")


def test_optional_int_zero():
    output = to_optional_int("0")
    assert output is None


def test_optional_int_none():
    output = to_optional_int(None)
    assert output is None


def test_optional_float():
    output = to_optional_float(1.23)
    assert output == "1.23"


def test_optional_float_str():
    output = to_optional_float("1.23")
    assert output == "1.23"


def test_optional_float_double_decimal():
    output = to_optional_float("1..23")
    assert output == "1.23"


def test_optional_float_invalid():
    with pytest.raises(ValueError):
        to_optional_float("Not Float")


def test_optional_float_zero():
    output = to_optional_float("0")
    assert output is None


def test_optional_float_none():
    output = to_optional_float(None)
    assert output is None


def test_optional_str():
    output = to_optional_str("String value")
    assert output == "String value"


def test_optional_str_none():
    output = to_optional_str(None)
    assert output is None


def test_bool_true():
    output = to_bool("1")
    assert output is True


def test_bool_false():
    output = to_bool("0")
    assert output is False


def test_bool_invalid():
    with pytest.raises(ValueError):
        to_bool("2")

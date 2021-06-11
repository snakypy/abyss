"""Tests for `abyss` package."""


import pytest

from snakypy.abyss import __info__


def test_version():
    assert __info__["version"] == "0.1.0"


def test_something_000():
    """Test Something"""
    assert (25 / 5) == 5
    with pytest.raises(ZeroDivisionError):
        assert (1 / 0) == 0

"""Tests for `abyss` package."""
from snakypy.abyss import __info__


def test_version():
    assert __info__["version"] == "0.1.0"


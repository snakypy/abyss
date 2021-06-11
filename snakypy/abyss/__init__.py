"""
abyss
~~~~~~~~~~~~~~~~~

Abyss is a toolkit for encrypting data and erasing data from certain directories.


For more information, access: 'https://github.com/snakypy/abyss'

:copyright: Copyright 2020-present, see AUTHORS.
:license: MIT license, see LICENSE for details.
"""
from os.path import abspath, dirname, join

from snakypy.helpers.files import eqversion

__info__ = {"name": "abyss", "version": "0.1.0", "organization": "Snakypy"}


# Keep the versions the same on pyproject.toml and __init__.py
pyproject = join(dirname(abspath(__file__)), "../..", "pyproject.toml")
eqversion(pyproject, __info__["version"])

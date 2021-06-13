"""CLI - Command Line Interface"""
from snakypy.helpers import FG, printer
from snakypy.helpers.catches import tools_requirements
from snakypy.helpers.console import credence
from snakypy.helpers.decorators import only_linux

from snakypy.abyss import __info__
from snakypy.abyss.config import Config
from snakypy.abyss.toolkit.encfs import Encfs
from snakypy.abyss.toolkit.shred import Shred
from snakypy.abyss.utils.base import Base
from snakypy.abyss.utils.functools import deny_user_permission
from snakypy.abyss.utils.menu import Menu


@only_linux
def main():
    if Menu().main().version:
        printer(f"{__info__['name']}:{FG().CYAN}", __info__["version"])
    elif Menu().main().credits:
        credence(__info__["name"], __info__["version"], __info__["home_page"], __info__, foreground=FG().CYAN)
    else:
        # Deny permission user by UID
        deny_user_permission(uid=0)
        # Tools requirements
        tools_requirements("shred", "encfs", "find")
        # Set configuration
        Config().set(Menu, Base().config_file)
        # Encfs run
        Encfs(Base().config_file).run(Menu, Base().config_file)
        # Shred run
        Shred(Base().config_file).run(Menu, Base().config_file)

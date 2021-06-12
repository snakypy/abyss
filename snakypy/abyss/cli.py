"""CLI - Command Line Interface"""
from snakypy.helpers.catches import tools_requirements

from snakypy.abyss.config import Config
from snakypy.abyss.toolkit.encfs import Encfs
from snakypy.abyss.utils.base import Base
from snakypy.abyss.utils.functools import deny_user_permission
from snakypy.abyss.utils.menu import Menu


def main():
    # Deny permission user by UID
    deny_user_permission(uid=0)
    # Tools requirements
    tools_requirements("shred", "encfs")
    # Set configuration
    Config().set(Menu(), Base().config_file)
    # Encfs run
    Encfs(Base().config_file).main(Menu(), Base().config_file)

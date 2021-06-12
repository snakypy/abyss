"""CLI - Command Line Interface"""
from snakypy.abyss.config import Config
from snakypy.abyss.kit.encfs import Encfs
from snakypy.abyss.utils.base import Base
from snakypy.abyss.utils.menu import Menu


def main():
    # Set configuration
    Config().set(Menu(), Base().config_file)
    # Encfs run
    Encfs(Base().config_file).main(Menu(), Base().config_file)

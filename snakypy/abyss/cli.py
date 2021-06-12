"""CLI - Command Line Interface"""
from snakypy.abyss.config import Config
from snakypy.abyss.kit.encfs import Encfs
from snakypy.abyss.utils import Base, Menu


def main():
    # Set configuration
    Config().set(Menu())
    # Encfs run
    Encfs(Base().config_file).main(Menu(), Base().config_file)

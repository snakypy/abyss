"""CLI - Command Line Interface"""
from snakypy.abyss.kit.encfs import Encfs
from snakypy.abyss.config import Config
from snakypy.abyss.utils import Menu


def main():
    Config().set(Menu())
    Encfs().main(Menu())

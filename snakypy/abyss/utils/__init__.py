from pathlib import Path
from os.path import join
from snakypy.abyss import __info__
from textwrap import dedent
from snakypy.helpers.files import read_json
from snakypy.abyss.config import Config
import argparse
from argparse import RawTextHelpFormatter
from snakypy.helpers import FG, NONE
from time import strftime
from contextlib import suppress


class Base:
    def __init__(self):
        self.HOME = str(Path.home())
        self.root_config = join(self.HOME, f".config/{__info__['name']}")
        self.config_file = join(self.HOME, self.root_config, "config.json")


class Menu(Base):
    def __init__(self):
        Base.__init__(self)
        self.parser = Config().get
        with suppress(FileNotFoundError):
            self.parser = read_json(self.config_file)

    def main(self):
        description_package = dedent(
            f"""
                {__info__["name"].title()} is a toolkit for encrypting data and erasing data from certain directories.
                """
        )
        arg_parser = argparse.ArgumentParser(
            description=f"{FG().MAGENTA}{description_package}{NONE}",
            usage=f" {__info__['name'].lower()} [-h]",
            formatter_class=RawTextHelpFormatter,
            epilog=f"(c) {strftime('%Y')} - {__info__['organization']}",
        )
        arg_parser.add_argument(
            "--config",
            metavar="ACTION",
            help="perform actions on the configuration file\n"
                 f"{FG().BLUE}ACTION             DESCRIPTION{NONE}\n"
                 "set             Create configuration file\n"
                 "open               Open configuration file\n"
                 "view               View configuration file\n"

        )
        if self.parser["encfs"]["enable"]:
            arg_parser.add_argument(
                "--encfs",
                metavar="ACTION",
                help="data encryption tool\n"
                     f"{FG().BLUE}ACTION             DESCRIPTION{NONE}\n"
                     "init               Creates the structure where the encrypted"
                     "and decrypted folder will be stored.\n"
                     "mount              Mount the encrypted folder\n"
                     "umount             Unmount the encrypted folder\n"
                     "status             Checks if encrypted folder is mounted\n"

            )
        if self.parser["zeroed"]["enable"]:
            arg_parser.add_argument(
                "--zeroed",
                help="",
            )
        return arg_parser.parse_args()

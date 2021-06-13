from contextlib import suppress
from os import environ, system
from subprocess import DEVNULL, call
from typing import Callable

from snakypy.helpers import FG, printer
from snakypy.helpers.files import read_json
from snakypy.helpers.os import cleaner, rmdir_blank

from snakypy.abyss.config import Config


class Shred:
    def __init__(self, config_file: str):
        self.parser: dict = Config().get
        with suppress(FileNotFoundError):
            self.parser = read_json(config_file)

    def secure(self, option: tuple = (), silent: bool = False):
        if option:
            steps: int = self.parser["shred"]["secure"]["steps"]
            if "trash" in option:
                path: str = self.parser["shred"]["secure"]["directories"]["trash"]
                path = path.replace("$HOME", environ["HOME"])
                cmd = f"find {path} -depth -type f -exec shred -v -n {str(steps)} -z -u {{}} \\;"
                call(cmd, shell=True, stderr=DEVNULL, stdout=DEVNULL) if silent else system(cmd)
                rmdir_blank(path)
            if "several" in option:
                several: list = self.parser["shred"]["secure"]["directories"]["several"]
                if several:
                    for path in several:
                        cmd = f"find {path} -depth -type f -exec shred -v -n {str(steps)} -z -u {{}} \\;"
                        call(cmd, shell=True, stderr=DEVNULL, stdout=DEVNULL) if silent else system(cmd)
                        rmdir_blank(path)

    def normal(self):
        paths: list = self.parser["shred"]["normal"]["directories"]
        if paths:
            for path in paths:
                cleaner(path, level=1)
                cleaner(path, level=2)

    def run(self, Menu: Callable, path: str):
        try:
            menu = Menu()
            Config().exists(path)
            if self.parser["shred"]["enable"]:
                if menu.main().shred == "trash":
                    self.secure(option=("trash",), silent=menu.main().silent)
                elif menu.main().shred == "secure":
                    self.secure(option=("trash", "several"), silent=menu.main().silent)
                elif menu.main().shred == "normal":
                    self.normal()
        except KeyboardInterrupt:
            printer("Aborted by user", foreground=FG().WARNING)
            exit(0)

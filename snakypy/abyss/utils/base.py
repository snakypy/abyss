from os.path import join
from pathlib import Path

from snakypy.abyss import __info__


class Base:
    def __init__(self):
        self.HOME: str = str(Path.home())
        self.root_config: str = join(self.HOME, f".config/{__info__['executable']}")
        self.config_file: str = join(self.HOME, self.root_config, "config.json")

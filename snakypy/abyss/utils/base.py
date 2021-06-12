from os.path import join
from pathlib import Path

from snakypy.abyss import __info__


class Base:
    def __init__(self):
        self.HOME = str(Path.home())
        self.root_config = join(self.HOME, f".config/{__info__['name']}")
        self.config_file = join(self.HOME, self.root_config, "config.json")

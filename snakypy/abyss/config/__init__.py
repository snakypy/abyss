from os.path import exists
from pydoc import pager
from sys import exit
from typing import Callable

from snakypy.helpers import FG, printer
from snakypy.helpers.files import create_json, read_file
from snakypy.helpers.path import create as create_path

from snakypy.abyss.utils.functools import editor_run


class Config:
    # TODO: Add multiple path ("path": []) in "encfs".
    @property
    def get(self) -> dict:
        return {
            "general": {"editor": "vim"},
            "shred": {
                "enable": False,
                "secure": {"steps": 2, "directories": {"trash": "$HOME/.local/share/Trash/files", "several": []}},
                "normal": {"directories": []},
            },
            "encfs": {
                "enable": False,
                "path": "$HOME/.encfs",
                "symlink": {"decrypted": "Open_Crypt"},
                "folder_name": {"decrypted": "show", "encrypted": "hide"},
            },
        }

    @staticmethod
    def exists(config_file: str):
        if not exists(config_file):
            printer('Configuration file does not exist. Use: "abyss --config create".', foreground=FG().ERROR)
            exit(1)

    def set(self, Menu: Callable, config: str):
        menu = Menu()
        if menu.main().config == "create":
            create_path(menu.root_config)
            try:
                create_json(self.get, menu.config_file)
            except FileExistsError:
                printer("The configuration file already exists.", foreground=FG().WARNING)
                exit(0)
        elif menu.main().config == "open":
            try:
                editor_current = Config().get["general"]["editor"]
                if editor_current:
                    editor_run(editor_current, config)
                else:
                    editors = ("vim", "nano", "emacs", "micro")
                    for edt in editors:
                        editor_run(edt, config)
            except FileNotFoundError:
                printer('Configuration file does not exist. Use: "abyss --config create".', foreground=FG().ERROR)
                exit(1)
        elif menu.main().config == "view":
            pager(read_file(config))
        elif menu.main().config == "reset":
            create_path(menu.root_config)
            create_json(self.get, menu.config_file, force=True)

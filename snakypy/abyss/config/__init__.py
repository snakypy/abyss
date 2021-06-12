from os.path import exists
from sys import exit

from snakypy.helpers import FG, printer
from snakypy.helpers.files import create_json
from snakypy.helpers.path import create as create_path

from snakypy.abyss.utils.functools import editor_run


class Config:
    # TODO: Add multiple path ("path": []) in "encfs".
    @property
    def get(self) -> dict:
        return {
            "general": {"editor": "vim"},
            "zeroed": {
                "enable": False,
                "delete_secure": [
                    "$HOME/.local/share/Trash/files/",
                ],
                "delete_normal": [],
            },
            "encfs": {
                "enable": False,
                "path": "$HOME/.encfs",
            },
        }

    @staticmethod
    def he_exists(config_file):
        if not exists(config_file):
            printer('Configuration file does not exist. Use: "abyss --config create".', foreground=FG().ERROR)
            exit(1)

    def set(self, menu, config):
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

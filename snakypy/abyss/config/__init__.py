from snakypy.helpers import printer, FG
from snakypy.helpers.files import create_json
from snakypy.helpers.path import create as create_path
from sys import exit
from os.path import exists


class Config:
    # TODO: Add multiple path ("path": []) in "encfs".
    @property
    def get(self) -> dict:
        return {
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

    def set(self, menu):
        if menu.main().config == "create":
            create_path(menu.root_config)
            try:
                create_json(self.get, menu.config_file)
            except FileExistsError:
                printer("The configuration file already exists.", foreground=FG().WARNING)
                exit(0)

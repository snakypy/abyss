from contextlib import suppress

from snakypy.helpers.files import create_json
from snakypy.helpers.path import create as create_path


class Config:
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

    def set(self, menu):
        if menu.main().config == "create":
            create_path(menu.root_config)
            with suppress(FileExistsError):
                create_json(self.get, menu.config_file)

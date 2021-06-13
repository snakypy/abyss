from contextlib import suppress
from os import environ, symlink, unlink
from os.path import isdir, join
from subprocess import run
from sys import exit
from typing import Callable

from snakypy.helpers import FG, NONE, printer
from snakypy.helpers.files import read_json
from snakypy.helpers.path import create as create_path

from snakypy.abyss import __info__
from snakypy.abyss.config import Config


class Encfs:
    def __init__(self, config_file: str):
        self.parser: dict = Config().get
        with suppress(FileNotFoundError):
            self.parser = read_json(config_file)
        self.decrypted = self.parser["encfs"]["folder_name"]["decrypted"]
        self.encrypted = self.parser["encfs"]["folder_name"]["encrypted"]
        self.symlink_decrypted = self.parser["encfs"]["symlink"]["decrypted"]

    def get_path(self) -> str:
        path: str = self.parser["encfs"]["path"]
        if "$HOME" in path:
            path = path.replace("$HOME", environ["HOME"])
        return path

    def verify_create(self):
        if not isdir(self.get_path()):
            printer(
                f'Repository not found. Run command: "{__info__["executable"]} --encfs create". Aborted!',
                foreground=FG().ERROR,
            )
            exit(1)

    def get_status(self) -> str:
        result = run(
            f'df -h | grep "{join(self.get_path(), self.decrypted)}"',
            shell=True,
            universal_newlines=True,
            capture_output=True,
        ).stdout
        return result

    def create(self):
        path = self.get_path()
        if isdir(path):
            printer(
                f'Repository already exists. Use: "{FG().MAGENTA}{__info__["executable"]} --encfs mount{NONE}".',
                foreground=FG().WARNING,
            )
        else:
            create_path(path, join(path, self.decrypted), join(path, self.encrypted))
            with suppress(FileNotFoundError):
                unlink(f"{join(environ['HOME'], self.symlink_decrypted)}")
            run(f"encfs {join(path, self.encrypted)} {join(path, self.decrypted)}", shell=True, universal_newlines=True)
            run(f"encfs -u {join(path, self.decrypted)}", shell=True, universal_newlines=True)
            printer("Repository created successfully.", foreground=FG().FINISH)

    def mount(self):
        self.verify_create()
        if self.get_status():
            printer("Repository is already set up.", foreground=FG().WARNING)
            exit(0)
        cmd = run(
            f"encfs {join(self.get_path(), self.encrypted)} {join(self.get_path(), self.decrypted)}",
            shell=True,
            universal_newlines=True,
            capture_output=True,
        )
        if "Error" in str(cmd.stdout):
            printer("Password incorrect. Aborted.", foreground=FG().ERROR)
            exit(1)
        with suppress(FileExistsError):
            symlink(join(self.get_path(), self.decrypted), join(environ["HOME"], self.symlink_decrypted))
        printer(
            f"Repository successfully mounted on: {FG().MAGENTA}\"{join(environ['HOME'], self.symlink_decrypted)}\"",
            foreground=FG().FINISH,
        )

    def umount(self):
        if not self.get_status():
            printer("There is no repository to disassemble.", foreground=FG().WARNING)
            exit(0)
        self.verify_create()
        path = self.get_path()
        run(f"encfs -u {join(path, self.decrypted)}", shell=True)
        with suppress(FileNotFoundError):
            unlink(f"{join(environ['HOME'], self.symlink_decrypted)}")
        printer("Repository umount successfully.", foreground=FG().FINISH)

    def status(self):
        if self.get_status():
            printer(f"Mounted in: {FG().MAGENTA}{join(environ['HOME'], self.symlink_decrypted)}", foreground=FG().CYAN)
        else:
            printer("There is no mounted repository.", foreground=FG().WARNING)

    def run(self, Menu: Callable, path: str):
        try:
            Config().exists(path)

            menu = Menu()
            if self.parser["encfs"]["enable"]:
                if menu.main().encfs == "create":
                    self.create()
                elif menu.main().encfs == "mount":
                    self.mount()
                elif menu.main().encfs == "umount":
                    self.umount()
                elif menu.main().encfs == "status":
                    self.status()
        except KeyboardInterrupt:
            printer("Aborted by user", foreground=FG().WARNING)
            exit(0)

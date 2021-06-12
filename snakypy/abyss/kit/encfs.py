from contextlib import suppress
from os import environ, symlink, unlink
from os.path import isdir, join
from subprocess import run
from sys import exit

from snakypy.helpers import FG, printer, NONE
from snakypy.helpers.files import read_json
from snakypy.helpers.path import create as create_path

from snakypy.abyss.config import Config


class Encfs:
    def __init__(self, config_file):
        self.parser: dict = Config().get
        with suppress(FileNotFoundError):
            self.parser: dict = read_json(config_file)

    def get_path(self) -> str:
        path: str = self.parser["encfs"]["path"]
        if "$HOME" in path:
            path = str(run("echo $HOME", shell=True, capture_output=True, universal_newlines=True).stdout.strip())
        return join(path, ".encfs")

    def verify_create(self):
        if not isdir(self.get_path()):
            printer('Repository not found. Run command: "abyss --encfs create". Aborted!', foreground=FG().ERROR)
            exit(1)

    def status(self) -> str:
        result = run(
            f'df -h | grep "{join(self.get_path(), "decrypted")}"',
            shell=True,
            universal_newlines=True,
            capture_output=True,
        ).stdout
        return result

    def create(self):
        path = self.get_path()
        if isdir(path):
            printer(
                f'Repository already exists. Use: "{FG().MAGENTA}abyss --encfs mount{NONE}".', foreground=FG().WARNING
            )
        else:
            create_path(path, join(path, "decrypted"), join(path, "encrypted"))
            with suppress(FileNotFoundError):
                unlink(f"{join(environ['HOME'], 'Encfs_ON')}")
            run(f'encfs {join(path, "encrypted")} {join(path, "decrypted")}', shell=True, universal_newlines=True)
            run(f'encfs -u {join(path, "decrypted")}', shell=True, universal_newlines=True)
            printer("Repository created successfully.", foreground=FG().FINISH)

    def mount(self):
        self.verify_create()
        if self.status():
            printer("Repository is already set up.", foreground=FG().WARNING)
            exit(0)
        cmd = run(
            f'encfs {join(self.get_path(), "encrypted")} {join(self.get_path(), "decrypted")}',
            shell=True,
            universal_newlines=True,
            capture_output=True,
        )
        if "Error" in str(cmd.stdout):
            printer("Password incorrect. Aborted.", foreground=FG().ERROR)
            exit(1)
        with suppress(FileExistsError):
            symlink(join(self.get_path(), "decrypted"), join(environ["HOME"], "Encfs_ON"))
        printer(
            f"Repository successfully mounted on: {FG().MAGENTA}\"{join(environ['HOME'], 'Encfs_ON')}\"",
            foreground=FG().FINISH,
        )

    def umount(self):
        if not self.status():
            printer("There is no repository to disassemble.", foreground=FG().WARNING)
            exit(0)
        self.verify_create()
        path = self.get_path()
        run(f'encfs -u {join(path, "decrypted")}', shell=True)
        with suppress(FileNotFoundError):
            unlink(f"{join(environ['HOME'], 'Encfs_ON')}")
        printer("Repository umount successfully.", foreground=FG().FINISH)

    def show_status(self):
        if self.status():
            printer(f"Mounted in: {FG().MAGENTA}{join(environ['HOME'], 'Encfs_ON')}", foreground=FG().CYAN)
        else:
            printer("Not mounted", foreground=FG().WARNING)

    def main(self, menu, path):
        Config().he_exists(path)

        if self.parser["encfs"]["enable"]:
            if menu.main().encfs == "create":
                self.create()
            elif menu.main().encfs == "mount":
                self.mount()
            elif menu.main().encfs == "umount":
                self.umount()
            elif menu.main().encfs == "status":
                self.show_status()

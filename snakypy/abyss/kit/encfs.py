from contextlib import suppress
from os import environ, symlink, unlink
from os.path import isdir, join
from subprocess import check_output, run
from sys import exit

from snakypy.helpers import FG, printer
from snakypy.helpers.files import read_json
from snakypy.helpers.path import create as create_path

from snakypy.abyss.config import Config
from snakypy.abyss.utils import Base


class Encfs(Base):
    def __init__(self):
        Base.__init__(self)
        self.parser: dict = Config().get
        with suppress(FileNotFoundError):
            self.parser: dict = read_json(self.config_file)

    def get_path(self) -> str:
        path: str = self.parser["encfs"]["path"]
        if "$HOME" in path:
            path = str(run("echo $HOME", shell=True, capture_output=True, universal_newlines=True).stdout.strip())
        return join(path, ".encfs")

    def verify_create(self):
        path = self.get_path()
        if not isdir(path):
            printer('Repository not found. Run command: "abyss --encfs create". Aborted!', foreground=FG().ERROR)
            exit(1)

    @staticmethod
    def status() -> str:
        result = check_output("df -h | grep encfs | awk '{ print $1 }'", shell=True, universal_newlines=True)
        return result

    def create(self):
        path = self.get_path()
        if isdir(path):
            printer("Repository already exists. Nothing to do.", foreground=FG().WARNING)
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
        path = self.get_path()
        cmd = run(
            f'encfs {join(path, "encrypted")} {join(path, "decrypted")}',
            shell=True,
            universal_newlines=True,
            capture_output=True,
        )
        if "Error" in str(cmd.stdout):
            printer("Password incorrect. Aborted.", foreground=FG().ERROR)
            exit(1)
        with suppress(FileExistsError):
            symlink(join(path, "decrypted"), join(environ["HOME"], "Encfs_ON"))
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

    def main(self, menu):
        if menu.main().encfs == "create":
            self.create()
        elif menu.main().encfs == "mount":
            self.mount()
        elif menu.main().encfs == "umount":
            self.umount()

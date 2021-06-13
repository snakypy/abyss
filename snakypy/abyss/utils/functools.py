from os import environ, geteuid
from shutil import which
from subprocess import call
from sys import exit
from typing import Union

from snakypy.helpers import FG, printer

from snakypy.abyss import __info__


def editor_run(editor: str, config: str) -> bool:
    if which(editor):
        get_editor = environ.get("EDITOR", editor)
        with open(config) as f:
            call([get_editor, f.name])
            return True
    return False


def deny_user_permission(uid: Union[None, int] = None):
    if uid and geteuid() == uid:
        printer(f'{__info__["name"]} can not be run with user UID {uid}. Aborted!', foreground=FG().ERROR)
        exit(1)

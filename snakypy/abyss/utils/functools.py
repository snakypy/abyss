from shutil import which
from subprocess import call
from os import environ


def editor_run(editor, config) -> bool:
    if which(editor):
        get_editor = environ.get("EDITOR", editor)
        with open(config) as f:
            call([get_editor, f.name])
            return True
    return False

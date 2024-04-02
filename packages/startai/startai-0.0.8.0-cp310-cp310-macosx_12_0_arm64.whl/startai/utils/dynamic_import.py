# NOQA
import startai
from importlib import import_module as builtin_import


def import_module(name, package=None):
    if startai.is_local():
        with startai.utils._importlib.LocalStartaiImporter():
            return startai.utils._importlib._import_module(name=name, package=package)
    return builtin_import(name=name, package=package)

import pathlib
from .lib_csv import *


def get_version() -> str:
    with open(str(pathlib.Path(__file__).parent / 'version.txt'), mode='r') as version_file:
        version = version_file.readline()
    return version


__title__ = 'lib_csv'
__version__ = get_version()
__name__ = 'lib_csv'

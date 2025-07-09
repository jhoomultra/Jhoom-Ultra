import glob
from os.path import basename, dirname, isfile

ALL_MODULES = sorted(
    [
        basename(f)[:-3]
        for f in glob.glob(dirname(__file__) + "/*.py")
        if isfile(f) and not f.endswith("__init__.py")
    ]
)
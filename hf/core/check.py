import glob
from os.path import isfile
from pathlib import Path

from . import w1


def check_single_file(file: Path):
    func = w1(file.name.lower())
    for line in file.read_text().strip().splitlines():
        tmp = line.split(maxsplit=1)
        if len(tmp) == 1:
            yield False, tmp[0]
            continue
        digest, path = tmp
        if not isfile(path):
            yield False, path
            continue
        yield digest == func(path), path


def check_multi_file(ext: str):
    func = w1(ext[1:])
    for file in glob.iglob(f'*{ext}'):
        file_no_ext = file.removesuffix(ext)
        if not isfile(file_no_ext):
            continue
        with open(file) as fp:
            digest = fp.read().strip()
        yield digest == func(file_no_ext), file_no_ext

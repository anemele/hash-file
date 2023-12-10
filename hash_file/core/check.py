import glob
from os.path import isfile, splitext
from pathlib import Path
from typing import Iterable

from . import w1

T_CHECK = Iterable[tuple[bool, str, str | None]]


def check_sum_file(file: Path | str) -> T_CHECK:
    file = Path(file)
    func = w1(file.name.lower())
    for line in file.read_text().strip().splitlines():
        tmp = line.split(maxsplit=1)
        if len(tmp) == 1:
            yield False, tmp[0], 'bad digest format'
            continue
        digest, path = tmp
        if not isfile(path):
            yield False, path, 'not a file'
            continue
        yield digest == func(path), path, None


def _check_file(file: str):
    try:
        tmp = next(glob.iglob(f'{file}.*'))
    except StopIteration:
        return False, file, 'no digest file'
    _, alg = splitext(tmp)
    with open(tmp) as fp:
        digest = fp.read().strip()
    return digest == w1(alg.lower()[1:])(file), file, None


def check_files(files: Iterable[str]) -> T_CHECK:
    for file in files:
        yield _check_file(file)

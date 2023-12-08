#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""Get hash of file(s)."""
import argparse
import glob
import hashlib
import os.path
from functools import partial
from itertools import chain
from typing import AnyStr

ALGORITHM_AVAILABLE = {
    'md5',
    'sha1',
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    # 'shake_128', 'shake_256', # a parameter `length` required
    'blake2b',
    'blake2s',
}
ALGORITHM_DEFAULT = 'md5'


def hash_file(file: AnyStr, func: str, caps: bool) -> str:
    with open(file, 'rb') as fp:
        # 3.11+
        hash_ = hashlib.file_digest(fp, func)
    digest = hash_.hexdigest()
    return digest.upper() if caps else digest


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='+', type=str, help='files')
    parser.add_argument('-a', type=str, help='algorithm')
    parser.add_argument('-c', action='store_true', help='capitalized')

    return parser.parse_args()


def main():
    args = parse_args()
    # print(args)
    # return
    a: str = args.a
    c: bool = args.c
    args_file: list[str] = args.file

    if a is None:
        algorithm = ALGORITHM_DEFAULT
    elif a not in ALGORITHM_AVAILABLE:
        print(f'[WARNING] {a} not available, use {ALGORITHM_DEFAULT} instead.')
        algorithm = ALGORITHM_DEFAULT
    else:
        algorithm = a

    hash_func = partial(hash_file, func=algorithm, caps=c)
    files = filter(os.path.isfile, chain.from_iterable(map(glob.iglob, args_file)))

    for file in files:
        print(f'{hash_func(file)}  {file}')


if __name__ == '__main__':
    main()

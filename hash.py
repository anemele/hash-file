#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

""" Get hash of file(s). """
import argparse
import glob
import hashlib
import os.path
from functools import partial
from itertools import chain
from typing import AnyStr, Callable

algorithm_available = ('md5', 'sha1', 'sha256', 'sha512')
algorithm_default = 'md5'
chunk_size = 1 << 20


def hash_file(file: AnyStr, func: Callable, caps: bool) -> str:
    hash_ = func()
    with open(file, 'rb') as fp:
        while True:
            if not (block := fp.read(chunk_size)):
                break
            hash_.update(block)
    hexdigest = hash_.hexdigest()
    return hexdigest.upper() if caps else hexdigest


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='+', type=str, help='files')
    parser.add_argument('-a', '--alg', type=str, help='hash algorithm')
    parser.add_argument('--caps', action='store_true', help='capital digest')

    return parser.parse_args()


def main():
    args = parse_args()
    # print(args)
    # return

    alg = args.alg
    if alg is None or alg not in algorithm_available:
        algorithm = algorithm_default
    else:
        algorithm = alg
    caps = args.caps
    file = args.file

    hash_func = partial(hash_file, func=getattr(hashlib, algorithm), caps=caps)
    files = filter(os.path.isfile, chain.from_iterable(map(glob.iglob, file)))

    for file in files:
        print(f'{hash_func(file)}  {file}')


if __name__ == '__main__':
    main()

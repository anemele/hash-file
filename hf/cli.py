import glob
import sys
from itertools import chain
from os.path import isfile
from pathlib import Path
from typing import Iterable

import click

from .core import w1, w2
from .core.check import check_multi_file, check_single_file
from .log import logger


class OrderedGroup(click.Group):
    def list_commands(self, _):
        return self.commands.keys()


@click.group(cls=OrderedGroup)
def cli():
    pass


def add_cmd(callback, name: str | None = None):
    cli.add_command(
        click.Command(
            name or callback.__name__,
            callback=callback,
            params=[
                click.Argument(['item'], nargs=-1, required=True),
                click.Option(
                    ['-t', '--text'],
                    is_flag=True,
                    default=False,
                    help='text mode: treat params as text',
                ),
                click.Option(
                    ['--encoding'],
                    default='utf-8',
                    show_default=True,
                    help='work with flag --text',
                ),
                click.Option(
                    ['--save'],
                    is_flag=True,
                    default=False,
                    help='redirect to single file. (not text mode)',
                ),
                click.Option(
                    ['--save2'],
                    is_flag=True,
                    default=False,
                    help='redirect to multi-files. (not text mode)',
                ),
            ],
        )
    )


def f(algorithm: str):
    def g(**kw):
        logger.debug(kw)

        item: tuple[str] = kw['item']

        if kw['text']:
            encoding: str = kw['encoding']
            func = w2(algorithm)
            for it in item:
                digest = func(it.encode(encoding))
                sys.stdout.write(f'{digest}  {it}\n')
        else:
            files = filter(isfile, chain.from_iterable(map(glob.iglob, item)))
            func = w1(algorithm)

            if kw['save']:
                data = '\n'.join(f'{func(i)}  {i}' for i in files)
                Path(algorithm.upper()).write_text(data)
            elif kw['save2']:
                for i in files:
                    Path(i).with_suffix(f'.{algorithm}').write_text(func(i))
            else:
                for d, i in map(func, files):
                    sys.stdout.write(f'{d}  {i}\n')

    g.__name__ = algorithm
    return g


add_cmd(f('md5'))
add_cmd(f('sha1'))
add_cmd(f('sha256'))
add_cmd(f('sha512'))
add_cmd(f('sha3_256'), 'sha3')


@cli.command(name='check')
@click.option('--file', type=Path, help='digest file with algorithm name')
@click.option('--ext', help='digest files with extension. (start with dot `.`)')
def check(file: Path | None = None, ext: str | None = None):
    """no message is good message"""
    logger.debug(f'{file=}')
    logger.debug(f'{ext=}')

    def pprint(check_result: Iterable[tuple[bool, str]]):
        for ok, path in check_result:
            logger.debug(f'{ok} {path}')
            if not ok:
                logger.info(f'bad file: {path}')

    if file is not None:
        pprint(check_single_file(file))
    if ext is not None:
        pprint(check_multi_file(ext))

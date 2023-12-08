import glob
import sys
from itertools import chain
from os.path import isfile
from pathlib import Path

import click

from .core import w1, w2
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
                    help='treat params as text',
                ),
                click.Option(
                    ['--encoding'],
                    default='utf-8',
                    show_default=True,
                    help='work with flag --text',
                ),
                click.Option(
                    ['-C', '--capital'],
                    is_flag=True,
                    default=False,
                    help='capitalize result',
                ),
                click.Option(
                    ['--save'],
                    is_flag=True,
                    default=False,
                    help='redirect to single file.',
                ),
                click.Option(
                    ['--save2'],
                    is_flag=True,
                    default=False,
                    help='redirect to multi file.',
                ),
            ],
        )
    )


def f(algorithm: str):
    def g(**kw):
        logger.debug(kw)

        item: tuple[str] = kw['item']
        capital: bool = kw['capital']

        if kw['text']:
            encoding: str = kw['encoding']
            func = w2(algorithm)
            for it in item:
                digest = func(it.encode(encoding), capital)
                sys.stdout.write(f'{digest}  {it}\n')
        else:
            files = filter(isfile, chain.from_iterable(map(glob.iglob, item)))
            func = w1(algorithm)

            data = ((func(it, capital), it) for it in files)

            if kw['save']:
                data = '\n'.join(f'{d}  {i}' for d, i in data)
                Path(algorithm.upper()).write_text(data)
            elif kw['save2']:
                data = tuple(data)
                for d, i in data:
                    Path(i).with_suffix(f'.{algorithm}').write_text(d)
            else:
                for d, i in data:
                    sys.stdout.write(f'{d}  {i}\n')

    g.__name__ = algorithm
    return g


add_cmd(f('md5'))
add_cmd(f('sha1'))
add_cmd(f('sha256'))
add_cmd(f('sha512'))
add_cmd(f('sha3_256'), 'sha3')

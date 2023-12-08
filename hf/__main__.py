import sys

from .cli import cli

cli(args=sys.argv[2:], prog_name=sys.argv[1])

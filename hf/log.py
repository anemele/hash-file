import logging
import sys

logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout,
)
logger = logging.getLogger(__package__)

"""
Using an artist ID discover all of their releases and find missing entries in
your library
"""

from .music_finder import MusicFinder
from ._finder_result import FinderResult


VERSION = (0, 1, 2)

VERSION_STRING = ".".join(map(str, VERSION))

MusicFinder

FinderResult

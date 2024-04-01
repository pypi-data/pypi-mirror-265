"""
Provides FinderResult dataclass
"""

from dataclasses import dataclass


@dataclass
class FinderResult():
    """Holds the artist name, mbid and any missing releases from the library
    MusicFinder was exected against
    """

    artist_name: str
    artist_mbid: str
    missing_releases: list[str]

    def __init__(self) -> None:
        pass

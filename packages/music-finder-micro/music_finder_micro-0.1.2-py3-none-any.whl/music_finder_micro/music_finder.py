"""
Provides class and functions to aid using a music ID as a base
 to find missing releases and related artists
"""

import os
import logging
import json
from sqlite3 import Cursor
from pathlib import Path
from music_brainz_api_micro import MusicBrainzAPI as MBAPI
from music_brainz_api_micro.cover_reponse import CoverResponse as CR
from music_validator_micro.music_validator import MusicValidator as MV
from ._database import DB
from ._finder_result import FinderResult as FR
from ._artist import Artist as A


class MusicFinder():
    """
    Used to discover missing releases for an artist
    """

    app_name = "MusicFinderMicro"
    debug: bool
    # Directory and files
    root_config_dir: str = os.path.join(
        str(Path.home()), ".config/", app_name)
    root_cache_dir: str = os.path.join(
        str(Path.home()), ".cache/", app_name)
    library_cache_file = 'library.db'
    active_library_config_dir: str
    active_library_cache_dir: str

    db: DB
    db_cursor: Cursor

    library: str

    mv: MV
    mb: MBAPI = MBAPI()
    artist_list: list[A]
    library_releases: list
    library_recordings: list[str]
    music_brainz_releases: list

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)

    def __init__(self,
                 library: str = 'library',
                 config_dir: str = None,
                 cache_dir: str = None,
                 debug: bool = False) -> None:
        """ Set up a new MusicFinder
        """
        self.debug = debug
        if config_dir:
            self.root_config_dir = config_dir
        if cache_dir:
            self.root_cache_dir = cache_dir
        self._set_library(library)
        self.mv = MV(library)
        self.db = DB(self.active_library_cache_dir)

    def _debug(self, message):
        if self.debug:
            logging.debug(str(message))

    def _set_library(self, library: str) -> None:
        self.library = library
        self._update_root_dir()

    def _update_root_dir(self) -> None:
        self.active_library_cache_dir = os.path.join(
            self.root_cache_dir,
            self.library,
            self.library_cache_file
        )
        Path(os.path.join(
            self.root_cache_dir,
            self.library
        )).mkdir(parents=True, exist_ok=True)

    def _save_list(self) -> None:
        pass

    def _build_artist_list(self) -> None:
        self.artist_list = []
        artist_mbids = self.mv.get_all_artist_mbid()
        for mbid in artist_mbids:
            artist = self.get_artist_by_mbid(mbid)
            if artist is not None:
                self.artist_list.append(artist)

    def get_artist_by_mbid(self, mbid) -> A | None:
        artist_response = self.mb.get_artist_by_mbid(mbid)
        if artist_response.error is False:
            respose_obj = json.loads(artist_response.response)
            return A(respose_obj['name'], mbid)
        return None

    def _update_artist_list(self) -> None:
        pass

    def _save_artist_list(self) -> None:
        for artist in self.artist_list:
            self.db.insert_artist(artist)

    def _save_releases(self) -> None:
        pass

    def _db_commit(self) -> None:
        self.db.db_commit()

    def get_all_covers(self) -> list[CR]:
        ret_val = []
        for r in self.library_recordings:
            is_cover = self.mb.get_recording_cover(r)
            if is_cover is not None:
                ret_val.append(is_cover)
        return ret_val

    def _get_library_recordings(self) -> None:
        self.library_recordings = self.mv.get_all_recording_mbid()

    def _get_library_releases(self) -> None:
        self.library_releases = self.mv.get_all_album_mbid()

    def _get_music_brainz_releases(self) -> None:
        self.music_brainz_releases = []
        for a in self.artist_list:
            release_response = self.mb.get_releases_by_artist(a.mbid)
            if release_response.error is False:
                release_obj = json.loads(release_response.response)
                releases = release_obj['release-groups']
                releases = {
                    'artist': a.name,
                    'mbid': a.mbid,
                    'releases': [x['id'] for x in releases]
                }
                self.music_brainz_releases.append(releases)

    def compare_releases(self) -> list[FR]:
        ret_val = []
        for a in self.music_brainz_releases:
            diff = list(set(a['releases']).difference(self.library_releases))
            self._debug(f"{a} {diff}")
            ret_val = [
                *ret_val, *diff]
        return ret_val

    def execute(self) -> list[FR]:
        self._build_artist_list()
        self._save_artist_list()
        self._get_library_releases()
        self._get_music_brainz_releases()
        self._save_releases()
        self._db_commit()
        return self.compare_releases()

    def get_result(self) -> list[FR]:
        pass
        # self._db_commit()

"""
Pytest test suite
"""
from music_manager_micro.music_manager import MusicManager as MM
from music_checker_micro import MusicChecker as MC
from music_validator_micro import MusicValidator as MV
from src.music_finder_micro import MusicFinder as MF
from src.music_finder_micro._artist import Artist as A


def test_covers():
    """
    Test class constructor
    """
    library = "###TESTMFCOVERS###"
    media_dir = "tests/test_covers"
    mm = MM(library, media_dir)
    mm.reset_library()
    mm_res = mm.execute()
    assert 4 == len(mm_res)
    mc = MC(library)
    mc_res = mc.execute()
    assert 4 == len(mc_res)
    mv = MV(library)
    mv_res = mv.execute()
    assert 4 == len(mv.get_all_artist_mbid())
    mf = MF(library)
    # mf.mb.root_url = "http://127.0.0.1:3000/"
    #mf.mb.clear_cache()
    assert 4 == len(mf.mv.get_all_artist_mbid())
    mf._build_artist_list()
    artist_list = mf.artist_list
    mf._get_library_recordings()
    recording_list = mf.library_recordings
    assert 3 == len(recording_list)
    covers = mf.get_all_covers()
    assert 2 == len(covers)


def test_music_finder_multiple():
    """
    Test class constructor
    """
    library = "###TESTMF###"
    media_dir = "tests/test_multiple_music"
    mm = MM(library, media_dir)
    mm.reset_library()
    mm_res = mm.execute()
    assert 2 == len(mm_res)
    mc = MC(library)
    mc_res = mc.execute()
    assert 2 == len(mc_res)
    mv = MV(library)
    mv_res = mv.execute()
    assert 2 == len(mv.get_all_artist_mbid())
    mf = MF(library)
    mf.mb.root_url = "http://127.0.0.1:3000/"
    mf.mb.clear_cache()
    assert 2 == len(mf.mv.get_all_artist_mbid())
    mf._build_artist_list()
    artist_list = mf.artist_list
    assert 2 == len(artist_list)
    assert isinstance(artist_list[0], A)
    compare_res = mf.execute()
    assert 4 == len(compare_res)
    assert '4f1e0d22-2557-4e37-901f-2dc6eaa6d16f' in compare_res


def test_music_finder():
    """
    Test class constructor
    """
    library = "###TESTMF###"
    media_dir = "tests/test_artist_music"
    mm = MM(library, media_dir)
    mm.reset_library()
    mm_res = mm.execute()
    assert 1 == len(mm_res)
    mc = MC(library)
    mc_res = mc.execute()
    assert 1 == len(mc_res)
    mv = MV(library)
    mv_res = mv.execute()
    # assert 1 == len(mv_res)
    assert 1 == len(mv.get_all_artist_mbid())
    mf = MF(library, debug=True)
    mf.mb.root_url = "http://127.0.0.1:3000/"
    mf.mb.clear_cache()
    assert 1 == len(mf.mv.get_all_artist_mbid())
    mf._build_artist_list()
    artist_list = mf.artist_list
    assert 1 == len(artist_list)
    assert isinstance(artist_list[0], A)
    mf._get_music_brainz_releases()
    release_list = mf.music_brainz_releases
    # assert 1 == release_list
    assert 1 == len(release_list)
    assert 2 == len(release_list[0]['releases'])
    mf._get_library_releases()
    library_release = mf.library_releases
    assert 1 == len(library_release)
    compare_res = mf.compare_releases()
    assert compare_res[0] == '4f1e0d22-2557-4e37-901f-2dc6eaa6d16f'


def test_get_artist_by_mbid():
    mbid = "1234"
    mf = MF()
    mf.mb.root_url = "http://127.0.0.1:3000/"
    artist = mf.get_artist_by_mbid(mbid)
    assert artist.name == "Victimized"

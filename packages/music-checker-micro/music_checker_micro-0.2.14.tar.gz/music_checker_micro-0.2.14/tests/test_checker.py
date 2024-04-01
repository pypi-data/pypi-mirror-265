"""
MusicCheckerMicro test cases
"""

from music_manager_micro.music_manager import MusicManager as MM
from src.music_checker_micro.music_checker import MusicChecker as MC
from src.music_checker_micro._music_file import MusicFile as MF
from src.music_checker_micro._database import db_entry_exists
from src.music_checker_micro._database import db_get_tag_dict
from src.music_checker_micro._database import db_get_all_paths
from src.music_checker_micro._database import db_entry_get_tags
from src.music_checker_micro._database import db_get_media_mtime


def test_ufid():
    """
    Testing UFID id3 tag extraction
    """
    library = "###TESTINGUFID###"
    library_dir = "./tests/mp3_ufid"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    ufid = mc.execute()
    assert ufid[0].tags['UFID:http://musicbrainz.org'] == '3456'


def test_db_entry_get_tags():
    """
    Testing of internal db get tags function
    """
    library = "###TESTING###"
    library_dir = "./tests/mp3_flac_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()

    get_tags = db_entry_get_tags(mc.db_cursor, mc.music_file_list[0])
    assert ('{"DATE": "2001", "TRACKNUMBER": "1", "ALBUM": "Album 1", '
            '"TITLE": "Track 1", "ARTIST": "Artist 1"}') == get_tags[
        0]


def test_get_db_mtime():
    """
    Testing of internal db get mtime function
    """
    library = "###TESTING###"
    library_dir = "./tests/mp3_flac_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()

    mtime = db_get_media_mtime(mc.db_cursor, mc.music_file_list[0])
    assert mtime == 1709479281.9321885
    assert mc.music_file_list[0].mtime == 1709479281.9321885


def test_multi_format():
    """
    Test to ensure all formats extract tags correctly 
    """
    library = "###TESTING###"
    library_dir = "./tests/mp3_flac_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    multi_format = mc.execute()
    assert multi_format[0].tags['ARTIST'] == "Artist 1"
    assert multi_format[1].tags['TPE1'] == "Artist 1"


def test_get_list():
    """
    Confirms the get_list function returns a cached value
    regardless of how music_manager updates
    """
    mm = MM("###TESTING###", "./tests/sample_mp3")
    mm.reset_library()
    mm.execute()
    mc = MC(library="###TESTING###")
    single_file = mc.execute()
    assert 1 == len(single_file)
    mm = MM("###TESTING###", "./tests/multi_sample")
    mm.reset_library()
    results = mc.get_list()
    assert 1 == len(results)


def test_all_entries():
    """
    test internal all_paths
    """
    mm = MM("###TESTING###", "./tests/sample_mp3")
    mm.reset_library()
    mm.execute()
    mc = MC(library="###TESTING###")
    single_file = mc.execute()
    paths = db_get_all_paths(mc.db_cursor)
    assert 1 == len(single_file)
    assert 1 == len(paths)

    # clean manager and rerun in multi file, confirm 2 files found
    mm.reset_library()
    mm = MM("###TESTING###", "./tests/multi_sample")
    multi_mp3 = mm.execute()
    assert 2 == len(multi_mp3)

    # run db util to confirm only 1 file still available
    mc = MC(library="###TESTING###")
    paths = db_get_all_paths(mc.db_cursor)
    assert 1 == len(paths)
    # confirm running checker updates files
    mc.execute()
    paths = db_get_all_paths(mc.db_cursor)
    assert 2 == len(paths)
    assert './tests/multi_sample/2.mp3' == paths[1][0]


def test_checker():
    """
    Full test of checker execute
    """
    mm = MM("###TESTING###", "./tests/sample_mp3")
    mm.reset_library()
    mm.execute()
    mc = MC(library="###TESTING###")
    result = mc.execute()
    assert 1 == len(result)
    assert './tests/sample_mp3' == result[0].path
    assert "sample.mp3" == result[0].file_name
    assert 'audio/mpeg' == result[0].file_type
    assert 'Album Example' == result[0].tags['TALB']


def test_checker_entry_exist():
    """
    internal entry_exists function
    """
    mc = MC(library="###TESTING###")
    mc.execute()
    entry = MF(
        path="./tests/sample_mp3",
        file_name="sample.mp3",
        mtime=1600000,
        file_type='',
        tags={},
        artwork=[]
    )
    is_exist = db_entry_exists(mc.db_cursor, entry)
    assert is_exist[0] == 1
    db_entry = db_get_tag_dict(mc.db_cursor, entry)
    assert isinstance(db_entry, dict)
    assert db_entry['TALB'] == "Album Example"


def test_checker_entry_not_exist():
    """
    entry_exists with an invalid entry
    """
    # mm = MM("###TESTING###")
    # single_mp3 = mm.execute("###TESTING###", "./tests/sample_mp3")
    mc = MC(library="###TESTING###")
    mc.execute()
    entry = MF(
        path="./tests/does_not_exist_sample_mp3",
        file_name="sample.mp3",
        mtime=1600000,
        file_type='',
        tags={},
        artwork=[]
    )
    is_exist = db_entry_exists(mc.db_cursor, entry)
    assert is_exist[0] == 0


def test_checker_use_mm():
    """
    Validate music_manager data works
    """
    mm = MM("###TESTING###", "./tests/empty_folder")
    mm.reset_library()
    zero_mp3 = mm.execute()
    assert len(zero_mp3) == 0
    mm = MM("###TESTING###", "./tests/sample_mp3")
    single_mp3 = mm.execute()
    assert len(single_mp3) == 1
    mc = MC(library="###TESTING###")
    media_list = mc.execute()
    assert len(media_list) == 1
    assert media_list[0].file_name == 'sample.mp3'

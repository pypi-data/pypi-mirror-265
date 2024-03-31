"""
Test suite for Validator
"""
from music_checker_micro.music_checker import MusicChecker as MC
from music_manager_micro.music_manager import MusicManager as MM
from src.music_validator_micro.music_validator import MusicValidator as MV


def test_custom_tag_map():
    library = "###TESTINGMVTAGMAP###"
    library_dir = "./tests/tagmap_samples"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm_res = mm.execute()
    mc = MC(library)
    mc_res = mc.execute()
    mv = MV(library, tag_list=['%%%Title', '%%%Album Artist'])
    mv_res = mv.execute()
    assert len(mv_res["%%%Album Artist"]) == 1
    assert len(mv_res["%%%Title"]) == 0


def test_get_all_mbid_multi_format():
    """
    Test of getting distinct mbid
    """
    library = "###TESTINGMVMBIDFORMAT###"
    library_dir = "./tests/mp3_flac_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm_res = mm.execute()
    mc = MC(library)
    mc_res = mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'TXXX:MusicBrainz Artist Id'])
    mv_res = mv.execute()
    mbids = mv.get_all_artist_mbid()
    assert mbids[0] == '1357'
    assert mbids[1] == '1234'


def test_get_all_mbid():
    """
    Test of getting distinct mbid
    """
    library = "###TESTINGMVMBID###"
    library_dir = "./tests/mbid_samples"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm_res = mm.execute()
    mc = MC(library)
    mc_res = mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'TXXX:MusicBrainz Artist Id'])
    mv_res = mv.execute()
    mbids = mv.get_all_artist_mbid()
    assert mbids[0] == '1234-5678-9012'
    assert mbids[1] == '1234-5678-9013'


def test_get_all_recording_mbid():
    """
    Test of getting distinct record mbid
    """
    library = "###TESTINGMVRECORD###"
    library_dir = "./tests/recording_mbid"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm_res = mm.execute()
    mc = MC(library)
    mc.INFO = True
    mc_res = mc.execute()
    mv = MV(library, tag_list=['talb', 'tit2', 'TXXX:MusicBrainz Artist Id'])
    mv_res = mv.execute()
    mbids = mv.get_all_recording_mbid()
    assert len(mbids) == 1
    assert mbids[0] == '4321'


def test_validator():
    """
    Full test of the music checker stack
    """

    library = "###TESTINGMV###"
    library_dir = "./tests/sample_mp3"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'ABC'])
    output = mv.execute()
    assert len(output.items()) == 3
    assert output['ABC'][0] == './tests/sample_mp3/sample.mp3'
    output = mv.get_list()
    assert len(output.items()) == 3
    assert output['ABC'][0] == './tests/sample_mp3/sample.mp3'


def test_multiple_validator():
    """
    Test of the validator with a directory containing more than
    one media file
    """

    library = "###TESTINGMVM###"
    library_dir = "./tests/multi_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'ABC'])
    output = mv.execute()
    assert len(output.items()) == 3
    assert len(output['ABC']) == 2
    assert './tests/multi_sample/2.mp3' in output['ABC']
    output = mv.get_list()
    assert len(output.items()) == 3
    assert len(output['ABC']) == 2
    assert './tests/multi_sample/2.mp3' in output['ABC']

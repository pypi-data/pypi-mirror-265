class TagMap():

    map: dict[dict] = {
        "%%%MusicBrainz Artist Id": {
            "audio/mpeg": "txxx:musicbrainz artist id",
            "audio/x-flac": "musicbrainz_artistid"
        },
        "%%%MusicBrainz Release Group Id": {
            "audio/mpeg": "txxx:musicbrainz release group id",
            "audio/x-flac": "musicbrainz_releasegroupid"
        },
        "%%%MusicBrainz Recording Id": {
            "audio/mpeg": "ufid:http://musicbrainz.org",
            "audio/x-flac": "musicbrainz_recordingid"
        },
        "%%%Album Artist": {
            "audio/mpeg": "tpe2",
            "audio/x-flac": "albumartist"
        },
        "%%%Title": {
            "audio/mpeg": "tit2",
            "audio/x-flac": "title"
        }
    }


"""
Provides DB functions
"""
import sqlite3
import os
import filetype
from ._music_file import MusicFile as MF
from ._generic_tag_map import TagMap


class DB():
    """
    Only need to instantiate once, not dependant on specific DB you are accessing 
    """

    cursor: sqlite3.Cursor

    def __init__(self) -> None:
        pass

    def instantiate_sqlite_table(self, file_name: str) -> sqlite3.Cursor:
        """Sets up the required sqlite db"""
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS track(
                    file_path type UNIQUE,
                    mtime,
                    file_type
                    )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS track_tag(
                    track,
                    tag,
                    value,
                    PRIMARY KEY (track, tag)
                    FOREIGN KEY (track)
                        REFERENCES track (ROWID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )
                    """)
        self.cursor = cur
        return cur

    def db_get_all_tracks(self) -> list[tuple[str, str]]:
        """Returns all values from the current db"""
        res = self.cursor.execute("SELECT * FROM track")
        ret_val = res.fetchall()
        # print(f'db_get_all ret val {ret_val}')
        return [] if ret_val is None else ret_val

    def db_get_track_tags(self, path: str) -> list[tuple]:
        """
        With a given file path returns a list of tuples of the tags.
        In the format of (path, tag name, tag value)
        """
        path = self.db_get_track_id(path)[0]
        sub_obj = {
            'file_path': path
        }
        res = self.cursor.execute(
            """
            SELECT *
            FROM track_tag
            WHERE track=:file_path
            """,
            sub_obj)
        ret_val = res.fetchall()
        return [] if ret_val is None else ret_val

    def db_get_all_tags(self) -> list:
        """Returns all the tag records from the db"""
        res = self.cursor.execute("SELECT * FROM track_tag")
        ret_val = res.fetchall()
        return [] if ret_val is None else ret_val

    def db_get_track_mtime(self, path: str) -> float | None:
        sub_obj = {
            "file_path": path
        }
        res = self.cursor.execute(
            """
            SELECT mtime
            FROM track
            WHERE file_path=:file_path
            """,
            sub_obj
        )
        ret_val = res.fetchone()
        return None if ret_val is None else ret_val[0]

    def db_get_distinct_record_mbid(self) -> list:
        ret_val = []
        for k, v in TagMap.map["%%%MusicBrainz Recording Id"].items():
            sub_obj = {
                "file_type": k,
                "tag": v
            }
            res = self.cursor.execute(
                """
                SELECT
                    l.tag,
                    l.value,
                    r.file_type
                FROM
                    track_tag l
                INNER JOIN track r ON
                    l.track = r.ROWID
                WHERE file_type=:file_type AND tag=:tag
                """,
                sub_obj)
            output = res.fetchall()
            ret_val = [*ret_val, *[x[1] for x in output]]
        return [] if ret_val is None else ret_val

    def db_get_distinct_album_mbid(self) -> list:
        ret_val = []
        for k, v in TagMap.map["%%%MusicBrainz Release Group Id"].items():
            sub_obj = {
                "file_type": k,
                "tag": v
            }
            res = self.cursor.execute(
                """
                SELECT
                    l.tag,
                    l.value,
                    r.file_type
                FROM
                    track_tag l
                INNER JOIN track r ON
                    l.track = r.ROWID
                WHERE file_type=:file_type AND tag=:tag
                """,
                sub_obj)
            output = res.fetchall()
            ret_val = [*ret_val, *[x[1] for x in output]]
        return [] if ret_val is None else ret_val

    def db_get_distinct_artist_mbid(self) -> list:
        ret_val = []
        for k, v in TagMap.map["%%%MusicBrainz Artist Id"].items():
            sub_obj = {
                "file_type": k,
                "tag": v
            }
            res = self.cursor.execute(
                """
                SELECT
                    l.tag,
                    l.value,
                    r.file_type
                FROM
                    track_tag l
                INNER JOIN track r ON
                    l.track = r.ROWID
                WHERE file_type=:file_type AND tag=:tag                             
                """,
                sub_obj)
            output = res.fetchall()
            ret_val = [*ret_val, *[x[1] for x in output]]
        return [] if ret_val is None else ret_val

    def mf_to_sub(self, entry: MF):
        """
        Converts a MusicFile object to a suitable dict for substitutions
        """
        file_path = os.path.join(entry.path, entry.file_name)
        sub = {
            'file_path': file_path,
            'mtime': entry.mtime
        }
        if entry.file_type is not None:
            sub['file_type'] = entry.file_type
        else:
            sub['file_type'] = filetype.guess(file_path).MIME
        return sub

    def db_insert_track(self, entry: MF):
        """Places an entry into the db with two values
        mtime and file_path from the tuple
        will match on file_path to update existing rows"""
        sub_obj = self.mf_to_sub(entry)
        self.cursor.execute(
            """
            INSERT INTO track(mtime,file_path,file_type) 
            VALUES (:mtime, :file_path, :file_type) 
            ON CONFLICT(file_path) 
            DO UPDATE SET mtime=:mtime, file_path=:file_path, file_type=:file_type
            """,
            sub_obj)

    def db_get_track_id(self,
                        file_path: str
                        ) -> str:
        sub_obj = {
            "file_path": file_path
        }
        res = self.cursor.execute(
            """
            SELECT ROWID
            FROM track
            WHERE file_path=:file_path
            """,
            sub_obj)
        ret_val = res.fetchone()
        return () if ret_val is None else ret_val

    def db_insert_tag(
            self,
            file_path: str,
            tag_name: str,
            tag_value: str) -> None:
        """
        Place a new tag entry related to a track, if the tag name
        already exists will update the value
        """

        track_id = self.db_get_track_id(file_path)[0]
        sub_obj = {
            "track": track_id,
            "tag": tag_name.lower(),
            "value": tag_value,
        }
        res = self.cursor.execute(
            """
            INSERT INTO track_tag(track, tag, value)
            VALUES(:track,:tag,:value)
            ON CONFLICT (track, tag)
            DO UPDATE SET value=:value
            """,
            sub_obj
        )

    def _db_delete_tags(self, path):
        pass

    def db_delete_track(self, path):
        """
        With a given file path will attempt to delete the track
        record. Cascade delete will remove related tags 
        """
        sub_obj = {
            "file_path": path
        }
        res = self.cursor.execute(
            """
            DELETE FROM track
            WHERE file_path=:file_path
            """,
            sub_obj
        )

    def _insert_tags(self, path):
        pass

    def db_commit(self) -> None:
        """Commits all outstanding statements"""
        self.cursor.connection.commit()

    def db_close(self) -> None:
        """Closes the connection"""
        self.cursor.connection.close()

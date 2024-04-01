"""
Provides DB functions
"""

import sqlite3
from sqlite3 import Cursor
from ._artist import Artist as A


class DB():
    """
    Provides SQLite database functions for MusicFinderMicro
    """

    cursor: Cursor

    def __init__(self, file_name: str) -> None:
        self.instantiate_sqlite_table(file_name)

    def instantiate_sqlite_table(self, file_name: str) -> Cursor:
        """Sets up the required SQLite db
        :param file_name: path and file name of db file
        :returns: The SQLite cursor relating to the DB
        """
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS library_artists(
                    mbid type UNIQUE,
                    name
                    )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS library_releases(
                    artist_mbid,
                    mbid type UNIQUE,
                    name, 
                    PRIMARY KEY (artist_mbid, mbid),
                    FOREIGN KEY (artist_mbid)
                        REFERENCES library_artist (ROWID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE                    
                    )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS mb_releases(
                    artist_mbid,
                    mbid type UNIQUE,
                    name,
                    PRIMARY KEY (artist_mbid, mbid),
                    FOREIGN KEY (artist_mbid)
                        REFERENCES library_artists (ROWID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE                    
                    )
                    """)
        self.cursor = cur
        return cur

    def delete_artist(self, artist: A) -> None:
        pass

    def insert_artist(self, artist: A) -> None:
        pass

    def db_commit(self) -> None:
        """Commits all outstanding statements"""
        self.cursor.connection.commit()

    def db_close(self) -> None:
        """Closes the connection"""
        self.cursor.connection.commit()

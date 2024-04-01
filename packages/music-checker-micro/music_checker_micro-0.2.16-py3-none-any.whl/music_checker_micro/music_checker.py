"""
Provides MusicChecker class
"""
from pathlib import Path

import logging
import os
import sqlite3

from music_manager_micro.music_manager import MusicManager as MM

from ._music_file import MusicFile as MF
from ._database import instantiate_sqlite_table, db_entry_exists, db_entry_get_tags, db_insert
from ._database import db_commit
from ._database import db_get_tag_dict
from ._database import db_get_all_paths
from ._database import db_delete_entry
from ._database import db_select_all
from ._database import db_get_media_mtime
from ._mutagen_handler import get_all_file_tags


class MusicChecker:
    """Class for functions to run tag checks against media files
    """
    # Constants
    # App specific props
    app_name = 'MusicCheckerMicro'

    # Directory and files
    config_dir: str = os.path.join(
        str(Path.home()), ".config/", app_name)
    cache_dir: str = os.path.join(
        str(Path.home()), ".cache/", app_name)
    cache_file: str = 'cache.db'

    # Variable
    # Session
    library: str = ''
    media_list: list[tuple[float, str, str]] = []
    music_file_list: list[MF] = []
    force_cache: bool = False
    db_cursor: sqlite3.Cursor
    force_recheck: bool = False

    _library_path = ''

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    DEBUG: bool = False
    INFO: bool = False

    def _debug(self, message):
        if self.DEBUG:
            logging.debug(str(message))

    def _info(self, message):
        if self.INFO:
            logging.info(str(message))

    ###
    # Init functions
    ###

    def __init__(self,
                 library: str = 'Library',
                 media_list: list | None = None,
                 cache_dir: str = None,
                 force_recheck: bool = False
                 ):
        self.force_recheck = force_recheck
        self._set_library(library)
        if cache_dir is not None:
            self.cache_dir = cache_dir
        if media_list is not None:
            self.media_list = media_list
        else:
            self.media_list = self._get_music_manager_list()

    def _generate_library_path(self) -> str:
        self._library_path = os.path.join(
            self.cache_dir, self.library, self.cache_file)
        path = Path(os.path.join(self.cache_dir, self.library))
        path.mkdir(parents=True, exist_ok=True)

    def _set_library(self, library: str) -> None:
        """Used to change the active library used by the class"""
        self.library = library
        self._generate_library_path()
        self.db_cursor = instantiate_sqlite_table(self._library_path)
    ###

    def _get_entry_tags(self, entry: MF):
        exists = db_entry_exists(self.db_cursor, entry)
        self._debug(f"_get_entry_tags - {entry.file_name} - exists {exists}")
        if int(exists[0]) == 0 or self.force_recheck is True:
            entry.tags, entry.file_type = get_all_file_tags(
                os.path.join(
                    entry.path,
                    entry.file_name
                )
            )
        else:

            db_tags = db_entry_get_tags(self.db_cursor, entry)
            self._debug(f"_get_entry_tags - db_tags {db_tags[0] is None}")
            if db_tags[0] is None:
                entry.tags, entry.file_type = get_all_file_tags(
                    os.path.join(
                        entry.path,
                        entry.file_name
                    )
                )
            else:
                db_mtime = db_get_media_mtime(self.db_cursor, entry)
                self._debug(
                    f"_get_entry_tags - mtime - {entry.mtime} {db_mtime}")
                if entry.mtime != db_mtime:
                    entry.tags, entry.file_type = get_all_file_tags(
                        os.path.join(
                            entry.path,
                            entry.file_name
                        )
                    )
                else:
                    entry.tags = db_get_tag_dict(self.db_cursor, entry)

        # if db_entry_exists(self.db_cursor, entry):
        #    entry.tags = db_entry_get_tags(self.db_cursor, entry)
        # else:
        #    entry.tags = get_all_mp3_id3_tags(entry.file_name)

    def _build_entry(self, media_file: tuple[float, str, str]) -> MF:
        """ Given a media file input builds a MusicFile entry for
        it

        :param media_file: Tuple providing the mtime and file path
            + name of the media file to generate 
        :returns: MusicFile representation
        """
        path = media_file[1].rsplit('/', 1)[0]
        file_name = media_file[1].split('/')[-1]
        mtime = media_file[0]
        if len(media_file) == 2:
            file_type = None
        else:
            file_type = media_file[2]
        entry = MF(
            path=path,
            file_name=file_name,
            mtime=mtime,
            file_type=file_type,
            tags={},
            artwork=[]
        )
        self._get_entry_tags(entry)
        return entry

    def _get_music_manager_list(self) -> list:
        mm = MM(self.library)
        # print(mm.get_list())
        return mm.get_list()

    def _build_list(self) -> list[MF]:
        """ Using the current media list builds an updated music
        file list

        :returns: list of MusicFiles        
        """
        music_file_list = []
        tot_entries = len(self.media_list)
        self._info(f"Building media list {tot_entries} entries")
        entry_iter = 0
        for m in self.media_list:
            entry_iter += 1
            if not entry_iter % 100:
                self._info(f"Processing entry {entry_iter} / {tot_entries}")
            music_file_list.append(self._build_entry(m))
        return music_file_list

    def execute_tag_finder(self) -> list:
        """Returns a list of unique tags found"""
        return_list = []

        return return_list

    def get_all_db_entries(self) -> list[str]:
        """ Gets all the file paths from the library db

        :returns: list of file paths
        """
        cur_entries = db_get_all_paths(self.db_cursor)
        return [x[0] for x in cur_entries]

    def remove_old_entries(self) -> None:
        """ Compares the list of media files and music files
        and finds entries no longer in the MusicFile list and
        removes them from the database

        """
        cur_entries = [x[1] for x in self.media_list]
        to_compare = [os.path.join(x.path, x.file_name)
                      for x in self.music_file_list]
        diff = list(set(to_compare).difference(cur_entries))
        for d in diff:
            db_delete_entry(self.db_cursor, d)

    def get_list(self) -> list[MF]:
        """ Gets the list of current music files from the database

        :returns: list of MusicFiles
        """
        all_music = db_select_all(self.db_cursor)
        self.music_file_list = []
        self._info(f"Getting existing db music {len(all_music)} entries")
        entry_iter = 0
        for a in all_music:
            entry_iter += 1
            if not entry_iter % 100:
                self._info(f"Processing entry {entry_iter}")
            self.music_file_list.append(self._build_entry(a))
        self._info(f"Found {len(self.music_file_list)} existing files")
        return self.music_file_list

    def save_list(self):
        """
        Saves music_file_list to the database
        """
        for m in self.music_file_list:
            db_insert(self.db_cursor, m)
        db_commit(self.db_cursor.connection)

    def _update_list(self):
        self.save_list()

    def _rebuild_list(self) -> None:
        self.music_file_list = self._build_list()

    def _compare_lists(self) -> None:
        # remove function to delete entries
        self.remove_old_entries()
        db_commit(self.db_cursor.connection)
        # rebuild from media_list
        self._rebuild_list()

    def execute(self) -> list[MF]:
        """Returns a list of tag values for each supported media file"""
        # get mm list
        # got in init so ignore
        self._info(f"Checking {len(self.media_list)} files")
        # get db list
        self.get_list()
        # compare
        self._compare_lists()
        # commit
        self._update_list()

        return self.music_file_list

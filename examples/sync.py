from stash import SqliteArchive
from trakt import Trakt
from trakt_sync.cache.backends import StashBackend
from trakt_sync.cache.enums import Media, Data
from trakt_sync.sync.main import Sync

import logging
import os
import sqlite3


def sync():
    conn = sqlite3.connect('sync.db')

    # SQLite storage interface for cache
    def storage(name):
        return StashBackend(
            SqliteArchive(conn, name), 'lru:///', 'pickle:///'
        )

    # Sync movies collection
    s = Sync(Media.All, Data.All, storage)
    s.run()

    s.save()

    pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    Trakt.configuration.defaults.client(
        id=os.environ['CLIENT_ID']
    )

    with Trakt.configuration.oauth(token=os.environ['ACCESS_TOKEN']):
        sync()

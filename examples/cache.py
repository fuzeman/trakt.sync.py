import logging

logging.basicConfig(level=logging.DEBUG)

from trakt_sync.cache.backends import StashBackend
from trakt_sync.cache.main import Cache

from stash import ApswArchive
from trakt import Trakt
import apsw
import os


def print_details(cache):
    for key in cache.collections.keys():
        print 'len(cache[%r]) = %d' % (key, len(cache[key]))


def flush(cache):
    cache.collections.flush()

    for store in cache.stores.values():
        store.flush()


if __name__ == '__main__':
    conn = apsw.Connection('cache.db', flags=apsw.SQLITE_OPEN_READWRITE | apsw.SQLITE_OPEN_CREATE | apsw.SQLITE_OPEN_WAL)

    # SQLite storage interface for cache
    def storage(name):
        return StashBackend(
            ApswArchive(conn, name), 'lru:///', 'pickle:///?protocol=2'
        )

    # Configure
    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    Trakt.configuration.defaults.http(
        retry=True
    )

    # Authenticate
    Trakt.configuration.defaults.oauth(
        token=os.environ.get('ACCESS_TOKEN')
    )

    # Retrieve account details
    settings = Trakt['users/settings'].get()
    username = (settings or {}).get('user', {}).get('username')

    # Build cache
    cache = Cache(Cache.Media.All, Cache.Data.All, storage)

    while True:
        # Refresh cache, print changes
        changes = cache.refresh(username)

        for (m, d), changes in changes:
            print m, d, changes

        print_details(cache)

        # Flush collection/stores to archives
        flush(cache)

        command = raw_input('[R, E]: ')

        if command == 'R':
            continue
        elif command == 'E':
            break

    # Flush collection/stores to archives
    flush(cache)

import logging
logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt
from trakt_sync.cache.backends import StashBackend
from trakt_sync.cache.main import Cache

from stash.archives.a_sqlite import SqliteArchive
import os
import sqlite3


def print_details(cache):
    movies = cache[(username, 'movies')]
    shows = cache[(username, 'shows')]

    print 'len(movies.archive) = %d ' % len(movies.archive)
    print 'len(movies.cache) = %d ' % len(movies.cache)

    print 'len(shows.archive) = %d ' % len(shows.archive)
    print 'len(shows.cache) = %d ' % len(shows.cache)

def save(cache):
    # Purge collection stores
    for key, collection in cache.collections.cache.items():
        collection['store'].save()

    # Purge collections
    cache.collections.save()


if __name__ == '__main__':
    conn = sqlite3.connect('stash_sqlite.db')

    # SQLite storage interface for cache
    def storage(name):
        return StashBackend(
            SqliteArchive(conn, name), 'lru:///', 'pickle:///'
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

    if not username:
        exit(1)

    # Build cache
    cache = Cache(Cache.Media.All, Cache.Data.All, storage)

    while True:
        cache.refresh(username)

        print_details(cache)
        save(cache)

        raw_input('[refresh]')

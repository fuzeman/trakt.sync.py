import logging
logging.basicConfig(level=logging.DEBUG)

from klepto._archives import sqlite_archive
from trakt import Trakt
from trakt_sync.cache.backends import KleptoBackend
from trakt_sync.cache.main import Cache
import os
import sqlite3


def print_details(cache):
    movies = cache[(username, 'movies')]
    shows = cache[(username, 'shows')]

    print 'len(cache[(%r, "movies")]) = %d' % (username, len(movies))
    print 'len(cache[(%r, "shows")]) = %d ' % (username, len(shows))

    # Display cache statistics
    for key, collection in cache.collections.items():
        print collection['store'].info()

    print cache.collections.info()


if __name__ == '__main__':
    conn = sqlite3.connect('klepto_sqlite.db')

    def i_storage(name):
        return KleptoBackend(
            archive=sqlite_archive(conn, name)
        )

    def purge_storage(cache):
        # Purge collection stores
        for key, collection in cache.collections.items():
            collection['store'].purge()

        # Purge collections
        cache.collections.purge()

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
    cache = Cache(Cache.Media.All, Cache.Data.All, i_storage)

    while True:
        cache.refresh(username)

        print_details(cache)

        purge_storage(cache)  # write cache to disk, clear items from memory

        raw_input('[refresh]')

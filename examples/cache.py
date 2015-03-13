import logging
logging.basicConfig(level=logging.DEBUG)

from trakt import Trakt
from trakt_sync.cache.main import Cache

import os


def print_details(cache):
    movies = cache[(username, 'movies')]
    shows = cache[(username, 'shows')]

    print 'len(cache[(%r, "movies")]) = %d' % (username, len(movies))
    print 'len(cache[(%r, "shows")]) = %d ' % (username, len(shows))


if __name__ == '__main__':
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
    storage = {}

    cache = Cache(storage, Cache.Media.All, Cache.Data.All)

    while True:
        cache.refresh(username)

        print_details(cache)
        raw_input('[refresh]')

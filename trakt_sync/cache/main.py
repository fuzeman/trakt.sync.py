from trakt import Trakt
from trakt.core.helpers import from_iso8601


class Cache(object):
    class Media(object):
        All         = 0x00
        Movies      = 0x01
        Shows       = 0x02
        Seasons     = 0x04
        Episodes    = 0x08

        __map__ = None

        @classmethod
        def get(cls, key):
            if cls.__map__ is None:
                cls.__map__ = {
                    Cache.Media.Movies:     'movies',
                    Cache.Media.Shows:      'shows',
                    Cache.Media.Seasons:    'seasons',
                    Cache.Media.Episodes:   'episodes'
                }

            return cls.__map__.get(key)

    class Data(object):
        All         = 0x00
        Collection  = 0x01
        Playback    = 0x02
        Ratings     = 0x04
        Watched     = 0x08
        Watchlist   = 0x16

        __attributes__ = None

        @classmethod
        def initialize(cls):
            if cls.__attributes__:
                return

            cls.__attributes__ = {
                Cache.Data.Collection: {
                    'interface': 'sync/collection',
                    'timestamp': 'collected_at'
                },
                Cache.Data.Playback: {
                    'interface': 'sync/playback',
                    'timestamp': 'paused_at'
                },
                Cache.Data.Ratings: {
                    'interface': 'sync/ratings',
                    'timestamp': 'rated_at'
                },
                Cache.Data.Watched: {
                    'interface': 'sync/watched',
                    'timestamp': 'watched_at'
                },
                Cache.Data.Watchlist: {
                    'interface': 'sync/watchlist',
                    'timestamp': 'watchlisted_at'
                }
            }

        @classmethod
        def get_interface(cls, key):
            return cls.get_attribute(key, 'interface')

        @classmethod
        def get_timestamp_key(cls, key):
            return cls.get_attribute(key, 'timestamp')

        @classmethod
        def get_attribute(cls, key, attribute):
            cls.initialize()

            attributes = cls.__attributes__.get(key)

            if not attributes:
                return None

            return attributes.get(attribute)

    def __init__(self, storage, media, data):
        self.storage = storage

        self.media = self._parse_enum(media, Cache.Media)
        self.data = self._parse_enum(data, Cache.Data)

    @classmethod
    def _parse_enum(cls, value, options):
        options = cls._parse_options(options)

        result = []

        for k, v in options.items():
            if type(v) is not int or v == 0:
                continue

            if value == 0 or (value & v) == v:
                result.append(v)

        return result

    @staticmethod
    def _parse_options(options):
        result = {}

        for key in dir(options):
            if key.startswith('_'):
                continue

            result[key] = getattr(options, key)

        return result

    def refresh(self, username):
        activities = Trakt['sync'].last_activities()

        for m in self.media:
            media = Cache.Media.get(m)

            for d in self.data:
                collection = self._get(username, media)

                timestamp_key = Cache.Data.get_timestamp_key(d)

                current = self._get_timestamp(activities, d, m)
                last = collection['timestamps'][media].get(timestamp_key)

                if last and last == current:
                    # Latest data already cached
                    continue

                if not self.fetch(username, d, m):
                    continue

                # Update timestamp in cache to `current`
                collection = self._get(username, media)
                collection['timestamps'][media][timestamp_key] = current

    def fetch(self, username, data, media):
        interface = Cache.Data.get_interface(data)
        method = Cache.Media.get(media)

        collection = self._get(username, method)

        # Retrieve function (`method`) from `interface`
        func = getattr(Trakt[interface], method, None)

        if func is None:
            return False

        # Execute `func` (fetch data from trakt.tv)
        print 'Fetching "%s"' % '/'.join([interface, method])

        try:
            func(store=collection['store'], exceptions=True)
        except Exception, ex:
            print type(ex), ex
            return False

        return True

    def __getitem__(self, key):
        if key not in self.storage:
            return None

        collection = self.storage[key]

        if 'store' not in collection:
            return None

        return collection['store']

    @staticmethod
    def _build_key(username, media):
        if media in ['seasons', 'episodes']:
            media = 'shows'

        return username, media

    def _get(self, username, media):
        key = self._build_key(username, media)

        if key not in self.storage:
            self.storage[key] = {}

        collection = self.storage[key]

        if 'store' not in collection:
            collection['store'] = {}

        if 'timestamps' not in collection:
            collection['timestamps'] = {}

        if media not in collection['timestamps']:
            collection['timestamps'][media] = {}

        return collection

    @staticmethod
    def _get_timestamp(activities, data, media):
        method = Cache.Media.get(media)

        if media in [Cache.Media.Movies, Cache.Media.Seasons, Cache.Media.Episodes]:
            timestamps = activities[method]
        elif media == Cache.Media.Shows:
            if data in [Cache.Data.Collection, Cache.Data.Playback, Cache.Data.Watched, Cache.Data.Watchlist]:
                # Map shows (collection, playback, watched, watchlist) -> episodes
                timestamps = activities['episodes']
            else:
                timestamps = activities[method]
        else:
            # unknown data/media combination
            raise ValueError()

        # Retrieve timestamp
        value = timestamps.get(
            Cache.Data.get_timestamp_key(data)
        )

        # Parse timestamp
        return from_iso8601(value)

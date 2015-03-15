import trakt_sync.cache.enums as enums

from trakt import Trakt
from trakt.core.helpers import from_iso8601


class Cache(object):
    Data = enums.Data
    Media = enums.Media

    def __init__(self, media, data, i_storage):
        self.i_storage = i_storage

        self.collections = self.i_storage('collections')
        self.stores = {}

        self.media = Cache.Media.parse(media)
        self.data = Cache.Data.parse(data)

    def refresh(self, username):
        activities = Trakt['sync'].last_activities()

        for m in self.media:
            media = Cache.Media.get(m)

            for d in self.data:
                collection = self._get_collection(username, media)

                timestamp_key = Cache.Data.get_timestamp_key(d)

                current = self._get_timestamp(activities, d, m)
                last = collection['timestamps'][media].get(timestamp_key)

                if last and last == current:
                    # Latest data already cached
                    continue

                if not self.fetch(username, d, m):
                    continue

                # Update timestamp in cache to `current`
                collection = self._get_collection(username, media)
                collection['timestamps'][media][timestamp_key] = current

    def fetch(self, username, data, media):
        interface = Cache.Data.get_interface(data)
        method = Cache.Media.get(media)

        collection = self._get_collection(username, method)

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
        if key not in self.collections:
            return None

        collection = self.collections[key]

        if 'store' not in collection:
            return None

        return collection['store']

    @staticmethod
    def _build_key(username, media):
        if media in ['seasons', 'episodes']:
            media = 'shows'

        return username, media

    def _get_collection(self, username, media):
        key = self._build_key(username, media)

        if key not in self.collections:
            self.collections[key] = {}

        collection = self.collections[key]

        collection['store'] = self._get_store(username, media)

        if 'timestamps' not in collection:
            collection['timestamps'] = {}

        if media not in collection['timestamps']:
            collection['timestamps'][media] = {}

        return collection

    def _get_store(self, username, media):
        key = self._build_key(username, media)

        if key not in self.stores:
            self.stores[key] = self.i_storage('stores.%s.%s' % (username, media))

        return self.stores[key]

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

from trakt_sync.cache.backends.core.base import Backend

from stash import Stash


class StashBackend(Backend):
    def __init__(self, archive, algorithm='lru:///', serializer='none:///'):
        self.stash = Stash(archive, algorithm, serializer, hash_key=self.hash_key)

    @property
    def archive(self):
        return self.stash.archive

    @property
    def cache(self):
        return self.stash.cache

    def flush(self):
        return self.stash.flush()

    def save(self):
        return self.stash.save()

    def __delitem__(self, key):
        return self.stash.__delitem__(key)

    def __getitem__(self, key):
        return self.stash.__getitem__(key)

    def __iter__(self):
        return self.stash.__iter__()

    def __len__(self):
        return self.stash.__len__()

    def __setitem__(self, key, value):
        return self.stash.__setitem__(key, value)

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    @staticmethod
    def hash_key(key):
        if type(key) is tuple:
            return '/'.join(key)

        return key

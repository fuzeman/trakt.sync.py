from klepto.tools import CacheInfo
from trakt_sync.cache.backends.core.base import Backend

from collections import deque
from klepto._archives import archive_dict
from klepto.keymaps import hashmap

try:
    from itertools import filterfalse
except ImportError:
    from itertools import ifilterfalse as filterfalse


class Counter(dict):
    """Mapping where default values are zero"""
    def __missing__(self, key):
        return 0


class KleptoBackend(Backend):
    def __init__(self, algorithm=None, archive=None):
        self.cache = (algorithm or LRU)(archive=archive)

    def __contains__(self, key):
        return self.cache.__contains__(key)

    def __getitem__(self, key):
        return self.cache[key]

    def __len__(self):
        return self.cache.__len__()

    def __setitem__(self, key, value):
        self.cache[key] = value

    def info(self):
        return self.cache.info()

    def items(self):
        return self.cache.items()

    def purge(self):
        return self.cache.purge()

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass


class LRU(object):
    def __init__(self, max_size=100, archive=None, keymap=None):
        self.max_size = max_size
        self.max_history = max_size * 10

        # Construct cache (with archive backend)
        self.cache = archive_dict(archive=archive) if archive is not None else archive_dict()
        self.keymap = keymap or hashmap(flat=True)

        self.history = deque()
        self.sentinel = object()

        self.references = Counter()

        self.stats = {'hit': 0, 'miss': 0, 'load': 0}

    def __contains__(self, key):
        key = self.keymap(key)

        if self.cache.__contains__(key):
            return True

        if self.cache.archived():
            # Try load item from archive
            self.cache.load(key)
        else:
            # No archive enabled, item doesn't exist
            return False

        return self.cache.__contains__(key)

    def __getitem__(self, key):
        key = self.keymap(key)

        # Try retrieve item
        try:
            result = self.cache[key]

            # Record recent use of this key
            self.history.append(key)
            self.references[key] += 1

            # Update statistics
            self.stats['hit'] += 1
        except KeyError:
            # Try load item from archive
            if self.cache.archived():
                self.cache.load(key)

            # Try retrieve item again
            try:
                result = self.cache[key]

                # Record recent use of this key
                self.history.append(key)
                self.references[key] += 1

                # Update statistics
                self.stats['load'] += 1
            except KeyError:
                result = None

                # Update statistics
                self.stats['miss'] += 1

            # purge cache
            if len(self.cache) > self.max_size:
                self.purge()

        # periodically compact the queue by eliminating duplicate keys
        # while preserving order of most recent access
        if len(self.history) > self.max_history:
            self.compact()

        return result

    def __len__(self):
        return self.cache.__len__()

    def __setitem__(self, key, value):
        key = self.keymap(key)

        self.cache[key] = value

        # Record recent use of this key
        self.history.append(key)
        self.references[key] += 1

        # purge cache
        if len(self.cache) > self.max_size:
            self.purge()

        # periodically compact the queue by eliminating duplicate keys
        # while preserving order of most recent access
        if len(self.history) > self.max_history:
            self.compact()

    def compact(self):
        self.references.clear()
        self.history.appendleft(self.sentinel)

        for key in filterfalse(self.references.__contains__,
                               iter(self.history.pop, self.sentinel)):
            self.history.appendleft(key)
            self.references[key] = 1

    def items(self):
        return self.cache.items()

    def purge(self):
        if self.cache.archived():
            # Dump everything to archive (and clear `history` and `references`)
            self.cache.dump()
            self.cache.clear()

            self.history.clear()
            self.references.clear()
            return

        # Purge least recently used cache entry
        key = self.history.popleft()
        self.references[key] -= 1

        while self.references[key]:
            key = self.history.popleft()
            self.references[key] -= 1

        del self.cache[key], self.references[key]

    def info(self):
        """Report cache statistics"""
        return CacheInfo(self.stats['hit'], self.stats['miss'], self.stats['load'], self.max_size, len(self.cache))

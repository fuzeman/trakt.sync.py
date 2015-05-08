from trakt import Trakt
from trakt_sync.cache.main import Cache


class Sync(object):
    def __init__(self, media, data, storage):
        self.cache = Cache(media, data, storage)

        self.settings = None
        self.username = None

    def initialize(self):
        # Settings
        if self.settings is None:
            self.settings = Trakt['users/settings'].get()

        if self.settings is None:
            return False

        # Username
        if self.username is None:
            self.username = self.settings.get('user', {}).get('username')

        if self.username is None:
            return False

        return True

    def run(self):
        self.initialize()

        # Refresh cache
        changes = self.cache.refresh(self.username)

        # collection = self.cache[('fuzeman-dev', 'movies')]
        # keys = collection.archive.keys()

        if changes:
            # Changes detected, update media center
            self.pull(changes)

        # TODO send changes to trakt.tv
        return

    def pull(self, changes):
        for (media, data), (added, removed) in changes:
            print '%r %r' % (media, data)

            print '\t- Added'
            for k, v in added.items():
                print '\t\t%r %r' % (k, v)

            print '\t- Removed'
            for k, v in removed.items():
                print '\t\t%r %r' % (k, v)

    def save(self):
        # Save collection stores
        for key, collection in self.cache.collections.cache.items():
            collection['store'].save()

        # Save collections
        self.cache.collections.save()

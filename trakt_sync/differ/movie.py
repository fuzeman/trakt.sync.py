from trakt_sync.differ.base import Differ


class MovieDiffer(Differ):
    def __init__(self, base, current):
        self.base = base
        self.current = current

        self.handlers = [
            h(self) for h in [
                Watched,
                Collection,
                Rating,
                Playback
            ]
        ]

        self.changes = {}

    def run(self):
        b = set(self.base.keys())
        c = set(self.current.keys())

        for key in c - b:
            self.process_added(self.current[key])

        for key in b - c:
            self.process_removed(self.base[key])

        for key in b & c:
            self.process_common(self.base[key], self.current[key])

        return self.changes

    def process_added(self, current):
        for h in self.handlers:
            h.on_added(current)

    def process_removed(self, base):
        for h in self.handlers:
            h.on_removed(base)

    def process_common(self, base, current):
        for h in self.handlers:
            h.on_common(base, current)

    def store(self, key, collection, action, properties=None):
        if collection not in self.changes:
            self.changes[collection] = {}

        if action not in self.changes[collection]:
            self.changes[collection][action] = {}

        self.changes[collection][action][key] = properties


class Handler(object):
    name = None

    def __init__(self, differ):
        self._differ = differ

    def on_added(self, current):
        pass

    def on_removed(self, base):
        pass

    def on_common(self, base, current):
        pass

    def properties(self, item):
        raise NotImplementedError()

    def properties_change(self, (base, current), attribute):
        return getattr(base, attribute), getattr(current, attribute)

    def store(self, key, collection, action, properties=None):
        return self._differ.store(key, collection, action, properties)

    def add(self, item):
        self.store(item.pk, self.name, 'added', self.properties(item))

    def remove(self, item):
        self.store(item.pk, self.name, 'removed', self.properties(item))

    def change(self, (base, current)):
        self.store(base.pk, self.name, 'changed', self.properties((base, current)))


class Watched(Handler):
    name = 'watched'

    def on_added(self, current):
        if current.is_watched is True:
            return self.add(current)

        if current.is_watched is False:
            return self.remove(current)

    def on_removed(self, base):
        if base.is_watched is True:
            return self.remove(base)

    def on_common(self, base, current):
        if base.is_watched == current.is_watched:
            return

        if base.is_watched is None:
            return self.add(current)

        if current.is_watched is None:
            return self.remove(base)

        return self.change((base, current))

    def properties(self, item):
        if type(item) is tuple:
            return {
                'is_watched': self.properties_change(item, 'is_watched'),

                'plays': self.properties_change(item, 'plays'),
                'last_watched_at': self.properties_change(item, 'last_watched_at')
            }

        return {
            'plays': item.plays,
            'last_watched_at': item.last_watched_at
        }


class Collection(Handler):
    name = 'collection'

    def on_added(self, current):
        if current.is_collected is True:
            return self.add(current)

        if current.is_collected is False:
            return self.remove(current)

    def on_removed(self, base):
        if base.is_collected is True:
            return self.remove(base)

    def on_common(self, base, current):
        if base.is_collected == current.is_collected:
            return

        if base.is_collected is None:
            return self.add(current)

        if current.is_collected is None:
            return self.remove(current)

        return self.change((base, current))

    def properties(self, item):
        if type(item) is tuple:
            return {
                'is_collected': self.properties_change(item, 'is_collected'),

                'collected_at': self.properties_change(item, 'collected_at')
            }

        return {
            'collected_at': item.collected_at
        }


class Rating(Handler):
    name = 'rating'

    def on_added(self, current):
        if current.rating is not None:
            return self.add(current)

    def on_removed(self, base):
        if base.rating is not None:
            return self.remove(base)

    def on_common(self, base, current):
        if base.rating == current.rating:
            return

        if base.rating is None:
            return self.add(current)

        if current.rating is None:
            return self.remove(current)

        return self.change((base, current))

    def properties(self, item):
        if type(item) is tuple:
            return {
                'rating': self.properties_change(item, 'rating')
            }

        return {
            'rating': item.rating
        }


class Playback(Handler):
    name = 'playback'

    def on_added(self, current):
        if current.progress is not None:
            return self.add(current)

    def on_removed(self, base):
        if base.progress is not None:
            return self.remove(base)

    def on_common(self, base, current):
        if base.progress == current.progress:
            return

        if base.progress is None:
            return self.add(current)

        if current.progress is None:
            return self.remove(current)

        return self.change((base, current))

    def properties(self, item):
        if type(item) is tuple:
            return {
                'progress': self.properties_change(item, 'progress'),

                'paused_at': self.properties_change(item, 'paused_at')
            }

        return {
            'progress': item.progress,

            'paused_at': item.paused_at
        }

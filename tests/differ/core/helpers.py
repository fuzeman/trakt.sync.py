from tests.core.helpers import read_json

from trakt import Trakt
from trakt.mapper.sync import SyncMapper
import pytest


def process(store, directory, media, **flags):
    path = 'differ/%s/%s.json' % (directory, media)

    SyncMapper.process(Trakt, store, read_json(path), media, **flags)


def load(directory, media):
    store = {}

    if media == 'shows':
        process(store, directory + '/collection', 'shows', is_collected=True)
        process(store, directory + '/playback', 'episodes')
        process(store, directory + '/ratings', 'episodes')
        process(store, directory + '/ratings', 'seasons')
        process(store, directory + '/ratings', 'shows')
        process(store, directory + '/watched', 'shows', is_watched=True)
    elif media == 'movies':
        process(store, directory + '/collection', 'movies', is_collected=True)
        process(store, directory + '/playback', 'movies')
        process(store, directory + '/ratings', 'movies')
        process(store, directory + '/watched', 'movies', is_watched=True)

    return store


def assert_matches(changes, keys, data):
    __tracebackhide__ = True

    for key in keys:
        if key not in changes:
            pytest.fail("Changes doesn't contain the %r key" % (key,))
            return False

        item = changes[key]

        if item != data:
            pytest.fail("Item %r doesn't match expected data %r" % (item, data))
            return False

    return True

from tests.core.helpers import read_json

from trakt.mapper.sync import SyncMapper


def process(store, directory, media, **flags):
    path = 'differ/%s/%s.json' % (directory, media)

    SyncMapper.process(store, read_json(path), media, **flags)


def load(directory, media):
    store = {}

    if media == 'shows':
        process(store, directory + '/collection', 'shows', is_collected=True)
        process(store, directory + '/playback', 'episodes')
        process(store, directory + '/ratings', 'episodes')
        process(store, directory + '/ratings', 'shows')
        process(store, directory + '/watched', 'shows', is_watched=True)
    elif media == 'movies':
        process(store, directory + '/collection', 'movies', is_collected=True)
        process(store, directory + '/playback', 'movies')
        process(store, directory + '/ratings', 'movies')
        process(store, directory + '/watched', 'movies', is_watched=True)

    return store

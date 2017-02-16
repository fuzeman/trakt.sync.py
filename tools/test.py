from trakt.mapper.sync import SyncMapper
from trakt_sync.differ import MovieDiffer
import json
import sys


def read(path):
    with open(path, 'rb') as fp:
        return fp.read()


def read_json(path):
    with open(path, 'rb') as fp:
        return json.load(fp)


def process(store, path, **flags):
    SyncMapper.process(None, store, read_json(path), 'movies', **flags)


def load(name):
    store = {}

    process(store, name + '/collection/movies.json', is_collected=True)
    process(store, name + '/watched/movies.json', is_watched=True)
    process(store, name + '/playback/movies.json')
    process(store, name + '/ratings/movies.json')

    return store

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(1)

    base_path = sys.argv[1]
    current_path = sys.argv[2]

    print "base_path: %r, current_path: %r" % (base_path, current_path)

    raw_input('[load]')

    # Load stores
    base = load(base_path)
    current = load(current_path)

    raw_input('[differ.run]')

    # Compare items
    differ = MovieDiffer(base, current)
    changes = differ.run()

    pass

from tests.core.helpers import read_json

from trakt.mapper.sync import SyncMapper
from trakt.objects import Rating
from trakt_sync.differ import MovieDiffer
import datetime


def test_basic_movies():
    def process(store, path, **flags):
        SyncMapper.process(store, read_json('differ/test_movie/basic/' + path), 'movies', **flags)

    def load(name):
        store = {}

        process(store, name + '/collection/movies.json', is_collected=True)
        process(store, name + '/watched/movies.json', is_watched=True)
        process(store, name + '/playback/movies.json')
        process(store, name + '/ratings/movies.json')

        return store

    # Load stores
    base = load('base')
    current = load('current')

    # Compare items
    differ = MovieDiffer(base, current)
    changes = differ.run()

    # Ensure changes are detected properly
    # - Watched
    assert changes['watched']['added'] == {
        ('imdb', 'tt2084970'): {'last_watched_at': datetime.datetime(2014, 4, 20, 12, 32, 59), 'plays': 1}
    }
    assert changes['watched']['removed'] == {
        ('imdb', 'tt1104001'): {'last_watched_at': datetime.datetime(2015, 1, 27, 23, 30, 16), 'plays': 1},
        ('imdb', 'tt2290065'): {'last_watched_at': datetime.datetime(2014, 4, 27, 13, 43, 59), 'plays': 2}
    }

    # - Collection
    assert changes['collection']['added'] == {
        ('imdb', 'tt0816692'): {'collected_at': datetime.datetime(2015, 5, 7, 1, 29, 23)}
    }
    assert changes['collection']['removed'] == {
        ('imdb', 'tt2290065'): {'collected_at': datetime.datetime(2014, 1, 20, 7, 4, 4)}
    }

    # - Rating
    assert changes['rating']['added'][('imdb', 'tt2084970')]['rating'] == Rating(7, datetime.datetime(2014, 11, 1, 0, 24, 54))

    assert changes['rating']['removed'][('imdb', 'tt2290065')]['rating'] == Rating(8, datetime.datetime(2015, 1, 28, 2, 26, 37))

    assert changes['rating']['changed'][('imdb', 'tt1170358')]['rating'] == (
        Rating(10, datetime.datetime(2014, 11, 1, 0, 24, 54)),
        Rating(8, datetime.datetime(2014, 11, 1, 0, 24, 54))
    )

    # - Playback
    assert changes['playback']['added'] == {
        ('imdb', 'tt2084970'): {'paused_at': datetime.datetime(2015, 2, 9, 5, 56, 58), 'progress': 69.0}
    }
    assert changes['playback']['removed'] == {
        ('imdb', 'tt2290065'): {'paused_at': datetime.datetime(2015, 1, 10, 6, 44, 9), 'progress': 0.0}
    }
    assert changes['playback']['changed'] == {
        ('imdb', 'tt1104001'): {
            'paused_at': (datetime.datetime(2015, 2, 9, 5, 56, 58), datetime.datetime(2015, 2, 9, 5, 56, 58)),
            'progress': (0.0, 65.0)
        }
    }

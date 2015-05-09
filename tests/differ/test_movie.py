from tests.differ.core.helpers import load

from trakt_sync.differ import MovieDiffer
import datetime
import pytest
import trakt.objects


@pytest.fixture(scope="module")
def changes():
    # Load stores
    base = load('test_movie/base', 'movies')
    current = load('test_movie/current', 'movies')

    # Compare items
    differ = MovieDiffer()

    return differ.run(base, current)


def test_watched(changes):
    # Ensure changes are detected properly
    assert changes['watched'] == {
        'removed': {
            ('imdb', 'tt1104001'): {'last_watched_at': datetime.datetime(2015, 1, 27, 23, 30, 16), 'plays': 1},
            ('imdb', 'tt2290065'): {'last_watched_at': datetime.datetime(2014, 4, 27, 13, 43, 59), 'plays': 2}
        },
        'added': {
            ('imdb', 'tt2084970'): {'last_watched_at': datetime.datetime(2014, 4, 20, 12, 32, 59), 'plays': 1}
        }
    }


def test_collection(changes):
    # Ensure changes are detected properly
    assert changes['collection'] == {
        'removed': {
            ('imdb', 'tt2290065'): {'collected_at': datetime.datetime(2014, 1, 20, 7, 4, 4)}
        },
        'added': {
            ('imdb', 'tt0816692'): {'collected_at': datetime.datetime(2015, 5, 7, 1, 29, 23)}
        }
    }


def test_rating(changes):
    # Ensure changes are detected properly
    assert changes['rating'] == {
        'removed': {
            ('imdb', 'tt2290065'): {'rating': trakt.objects.Rating(8, datetime.datetime(2015, 1, 28, 2, 26, 37))}
        },
        'added': {
            ('imdb', 'tt2084970'): {'rating': trakt.objects.Rating(7, datetime.datetime(2014, 11, 1, 0, 24, 54))}
        },
        'changed': {
            ('imdb', 'tt1170358'): {
                'rating': (
                    trakt.objects.Rating(10, datetime.datetime(2014, 11, 1, 0, 24, 54)),
                    trakt.objects.Rating(8, datetime.datetime(2014, 11, 1, 0, 24, 54))
                )
            }
        }
    }


def test_playback(changes):
    # Ensure changes are detected properly
    assert changes['playback'] == {
        'removed': {
            ('imdb', 'tt2290065'): {'progress': 0.0, 'paused_at': datetime.datetime(2015, 1, 10, 6, 44, 9)}
        },
        'added': {
            ('imdb', 'tt2084970'): {'progress': 69.0, 'paused_at': datetime.datetime(2015, 2, 9, 5, 56, 58)}
        },
        'changed': {
            ('imdb', 'tt1104001'): {
                'progress': (
                    0.0,
                    65.0
                ),
                'paused_at': (
                    datetime.datetime(2015, 2, 9, 5, 56, 58),
                    datetime.datetime(2015, 2, 9, 5, 56, 58)
                )
            }
        }
    }

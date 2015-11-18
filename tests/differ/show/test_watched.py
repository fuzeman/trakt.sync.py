from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt_sync.differ import ShowDiffer
import datetime
import pytest


@pytest.fixture(scope="module")
def changes():
    # Load stores
    base = load('test_show/base', 'shows')
    current = load('test_show/current', 'shows')

    # Compare items
    differ = ShowDiffer()
    result = differ.run(base, current)

    if not result:
        return None

    return result.changes


def test_added(changes):
    assert_matches(changes['watched']['added'], [
        ('imdb', 'tt1266020'),
        ('tmdb', '8592'),
        ('tvdb', '84912'),
        ('tvrage', '21686')
    ], {
        'seasons': {
            5: {
                'episodes': {
                    2: {'last_watched_at': datetime.datetime(2015, 1, 28, 20, 26, 15, tzinfo=tzutc()), 'plays': 3}
                }
            }
        }
    })

    assert_matches(changes['watched']['added'], [
        ('imdb', 'tt0934814'),
        ('tmdb', '1404'),
        ('tvdb', '80348'),
        ('tvrage', '15614')
    ], {
        'seasons': {
                1: {
                'episodes': {
                    2: {'last_watched_at': datetime.datetime(2015, 3, 10, 5, 21, 51, tzinfo=tzutc()), 'plays': 9},
                    4: {'last_watched_at': datetime.datetime(2015, 1, 29, 11, 29, 50, tzinfo=tzutc()), 'plays': 1}
                }
            }
        }
    })


def test_removed(changes):
    assert_matches(changes['watched']['removed'], [
        ('imdb', 'tt1266020'),
        ('tmdb', '8592'),
        ('tvdb', '84912'),
        ('tvrage', '21686')
    ], {
        'seasons': {
            6: {
                'episodes': {
                    1: {'last_watched_at': datetime.datetime(2014, 4, 14, 8, 4, 13, tzinfo=tzutc()), 'plays': 1}
                }
            }
        }
    })

    assert_matches(changes['watched']['removed'], [
        ('imdb', 'tt0496424'),
        ('tmdb', '4608'),
        ('tvdb', '79488'),
        ('tvrage', '11215')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    1: {'last_watched_at': datetime.datetime(2015, 1, 26, 5, 37, 3, tzinfo=tzutc()), 'plays': 1},
                    2: {'last_watched_at': datetime.datetime(2015, 2, 24, 0, 50, 41, tzinfo=tzutc()), 'plays': 1},
                    3: {'last_watched_at': datetime.datetime(2015, 2, 28, 1, 16, 26, tzinfo=tzutc()), 'plays': 1}
                }
            }
        }
    })

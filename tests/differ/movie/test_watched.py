from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt_sync.differ import MovieDiffer
import datetime
import pytest


@pytest.fixture(scope="module")
def changes():
    # Load stores
    base = load('test_movie/base', 'movies')
    current = load('test_movie/current', 'movies')

    # Compare items
    differ = MovieDiffer()
    result = differ.run(base, current)

    if not result:
        return None

    return result.changes


def test_added(changes):
    assert_matches(changes['watched']['added'], [
        ('imdb', 'tt2084970'),
        ('tmdb', '205596')
    ], {
        'last_watched_at': datetime.datetime(2014, 4, 20, 12, 32, 59, tzinfo=tzutc()),
        'plays': 1
    })


def test_removed(changes):
    assert_matches(changes['watched']['removed'], [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526')
    ], {
        'last_watched_at': datetime.datetime(2015, 1, 27, 23, 30, 16, tzinfo=tzutc()),
        'plays': 1
    })

    assert_matches(changes['watched']['removed'], [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757')
    ], {
        'last_watched_at': datetime.datetime(2014, 4, 27, 13, 43, 59, tzinfo=tzutc()),
        'plays': 2
    })

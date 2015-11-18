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
    assert_matches(changes['collection']['added'], [
        ('imdb', 'tt0816692'),
        ('tmdb', '157336')
    ], {
        'collected_at': datetime.datetime(2015, 5, 7, 1, 29, 23, tzinfo=tzutc())
    })


def test_removed(changes):
    assert_matches(changes['collection']['removed'], [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757')
    ], {
        'collected_at': datetime.datetime(2014, 1, 20, 7, 4, 4, tzinfo=tzutc())
    })

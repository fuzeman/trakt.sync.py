from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt_sync.differ import MovieDiffer
import datetime
import pytest


@pytest.fixture(scope="module")
def changes():
    # Load stores
    base = load('movie/base', 'movies')
    current = load('movie/current', 'movies')

    # Compare items
    differ = MovieDiffer()
    result = differ.run(base, current)

    if not result:
        return None

    return result.changes


def test_added(changes):
    assert_matches(changes['playback']['added'], [
        ('imdb', 'tt2084970'),
        ('tmdb', '205596')
    ], {
        'progress': 69.0,
        'paused_at': datetime.datetime(2015, 2, 9, 5, 56, 58, tzinfo=tzutc())
    })


def test_changed(changes):
    assert_matches(changes['playback']['changed'], [
        ('imdb', 'tt1104001'),
        ('tmdb', '20526')
    ], {
        'progress': (
            0.0,
            65.0
        ),
        'paused_at': (
            datetime.datetime(2015, 2, 9, 5, 56, 58, tzinfo=tzutc()),
            datetime.datetime(2015, 2, 9, 5, 56, 58, tzinfo=tzutc())
        )
    })


def test_removed(changes):
    assert_matches(changes['playback']['removed'], [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757')
    ], {
        'progress': 0.0,
        'paused_at': datetime.datetime(2015, 1, 10, 6, 44, 9, tzinfo=tzutc())
    })

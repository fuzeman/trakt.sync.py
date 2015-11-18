from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt import Trakt
from trakt_sync.differ import MovieDiffer
import datetime
import pytest
import trakt.objects


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
    assert_matches(changes['ratings']['added'], [
        ('imdb', 'tt2084970'),
        ('tmdb', '205596')
    ], {
        'rating': trakt.objects.Rating(Trakt, 7, datetime.datetime(2014, 11, 1, 0, 24, 54, tzinfo=tzutc()))
    })


def test_changed(changes):
    assert_matches(changes['ratings']['changed'], [
        ('imdb', 'tt1170358'),
        ('tmdb', '57158')
    ], {
        'rating': (
            trakt.objects.Rating(Trakt, 10, datetime.datetime(2014, 11, 1, 0, 24, 54, tzinfo=tzutc())),
            trakt.objects.Rating(Trakt, 8, datetime.datetime(2014, 11, 1, 0, 24, 54, tzinfo=tzutc()))
        )
    })


def test_removed(changes):
    assert_matches(changes['ratings']['removed'], [
        ('imdb', 'tt2290065'),
        ('tmdb', '126757')
    ], {
        'rating': trakt.objects.Rating(Trakt, 8, datetime.datetime(2015, 1, 28, 2, 26, 37, tzinfo=tzutc()))
    })

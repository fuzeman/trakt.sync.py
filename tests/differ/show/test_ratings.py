from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt import Trakt
from trakt_sync.differ import ShowDiffer
import datetime
import pytest
import trakt.objects


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
    assert_matches(changes['ratings']['added'], [
        ('imdb', 'tt0386676'),
        ('tmdb', '2316'),
        ('tvdb', '73244')
    ], {
        'seasons': {
            4: {
                'episodes': {
                    2: {'rating': trakt.objects.Rating(Trakt, 10, datetime.datetime(2015, 1, 7, 8, 31, 54, tzinfo=tzutc()))}
                }
            }
        }
    })

    assert_matches(changes['ratings']['added'], [
        ('imdb', 'tt0496424'),
        ('tmdb', '4608'),
        ('tvdb', '79488'),
        ('tvrage', '11215')
    ], {
        'rating': trakt.objects.Rating(Trakt, 8, datetime.datetime(2014, 10, 19, 23, 2, 23, tzinfo=tzutc()))
    })


def test_changed(changes):
    assert_matches(changes['ratings']['changed'], [
        ('imdb', 'tt1486217'),
        ('tmdb', '10283'),
        ('tvdb', '110381'),
        ('tvrage', '23354')
    ], {
        'seasons': {
            3: {
                'episodes': {
                    1: {'rating': (
                        trakt.objects.Rating(Trakt, 8, datetime.datetime(2015, 1, 17, 4, 35, 22, tzinfo=tzutc())),
                        trakt.objects.Rating(Trakt, 6, datetime.datetime(2015, 1, 17, 4, 35, 22, tzinfo=tzutc()))
                    )}
                }
            }
        }
    })

    assert_matches(changes['ratings']['changed'], [
        ('imdb', 'tt0386676'),
        ('tmdb', '2316'),
        ('tvdb', '73244')
    ], {
        'rating': (
            trakt.objects.Rating(Trakt, 10, datetime.datetime(2014, 11, 1, 0, 26, 18, tzinfo=tzutc())),
            trakt.objects.Rating(Trakt, 8, datetime.datetime(2014, 11, 1, 0, 26, 18, tzinfo=tzutc()))
        ),
        'seasons': {
            4: {
                'episodes': {
                    1: {'rating': (
                        trakt.objects.Rating(Trakt, 10, datetime.datetime(2015, 1, 7, 8, 31, 54, tzinfo=tzutc())),
                        trakt.objects.Rating(Trakt, 8, datetime.datetime(2015, 1, 7, 8, 31, 54, tzinfo=tzutc()))
                    )}
                }
            }
        }
    })

    assert_matches(changes['ratings']['changed'], [
        ('imdb', 'tt0934814'),
        ('tmdb', '1404'),
        ('tvdb', '80348'),
        ('tvrage', '15614')
    ], {
        'rating': (
            trakt.objects.Rating(Trakt, 8, datetime.datetime(2014, 10, 19, 23, 2, 23, tzinfo=tzutc())),
            trakt.objects.Rating(Trakt, 10, datetime.datetime(2014, 10, 19, 23, 2, 23, tzinfo=tzutc()))
        )
    })


def test_removed(changes):
    assert_matches(changes['ratings']['removed'], [
        ('imdb', 'tt0934814'),
        ('tmdb', '1404'),
        ('tvdb', '80348'),
        ('tvrage', '15614')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    1: {'rating': trakt.objects.Rating(Trakt, 10, datetime.datetime(2014, 10, 19, 23, 2, 24, tzinfo=tzutc()))}
                }
            }
        }
    })

    assert_matches(changes['ratings']['removed'], [
        ('imdb', 'tt2356777'),
        ('tmdb', '46648'),
        ('tvdb', '270633'),
        ('tvrage', '31369')
    ], {
        'rating': trakt.objects.Rating(Trakt, 6, datetime.datetime(2014, 5, 10, 0, 23, 37, tzinfo=tzutc()))
    })

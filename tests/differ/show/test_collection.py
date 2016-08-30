from tests.differ.core.helpers import assert_matches, load

from dateutil.tz import tzutc
from trakt_sync.differ import ShowDiffer
import datetime
import pytest


@pytest.fixture(scope="module")
def changes():
    # Load stores
    base = load('show/base', 'shows')
    current = load('show/current', 'shows')

    # Compare items
    differ = ShowDiffer()
    result = differ.run(base, current)

    if not result:
        return None

    return result.changes


def test_added(changes):
    assert_matches(changes['collection']['added'], [
        ('imdb', 'tt1266020'),
        ('tmdb', '8592'),
        ('tvdb', '84912'),
        ('tvrage', '21686')
    ], {
        'seasons': {
            6: {
                'episodes': {
                    2: {'collected_at': datetime.datetime(2014, 2, 15, 5, 35, 30, tzinfo=tzutc())}
                }
            }
        }
    })

    assert_matches(changes['collection']['added'], [
        ('imdb', 'tt1800864'),
        ('tmdb', '34634'),
        ('tvdb', '208111'),
        ('tvrage', '26961')
    ], {
        'seasons': {
            0: {
                'episodes': {
                    1: {'collected_at': datetime.datetime(2014, 9, 15, 1, 50, tzinfo=tzutc())}
                }
            }
        }
    })

    assert_matches(changes['collection']['added'], [
        ('imdb', 'tt0496424'),
        ('tmdb', '4608'),
        ('tvdb', '79488'),
        ('tvrage', '11215')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    2: {'collected_at': datetime.datetime(2013, 10, 11, 7, 41, 56, tzinfo=tzutc())}
                }
            }
        }
    })

    assert_matches(changes['collection']['added'], [
        ('imdb', 'tt2356777'),
        ('tmdb', '46648'),
        ('tvdb', '270633'),
        ('tvrage', '31369')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    1: {'collected_at': datetime.datetime(2014, 1, 29, 12, 56, 35, tzinfo=tzutc())}
                }
            }
        }
    })


def test_removed(changes):
    assert_matches(changes['collection']['removed'], [
        ('imdb', 'tt2240991'),
        ('tmdb', '45482'),
        ('tvdb', '260750')
    ], {
        'seasons': {
            2: {
                'episodes': {
                    2: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52, tzinfo=tzutc())}
                }
            },
            3: {
                'episodes': {
                    1: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52, tzinfo=tzutc())},
                    2: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52, tzinfo=tzutc())}
                }
            }
        }
    })
3
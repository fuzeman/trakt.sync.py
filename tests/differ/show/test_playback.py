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
    assert_matches(changes['playback']['added'], [
        ('imdb', 'tt2240991'),
        ('tmdb', '45482'),
        ('tvdb', '260750')
    ], {
        'seasons': {
            2: {
                'episodes': {
                    1: {'progress': 0.68, 'paused_at': datetime.datetime(2015, 3, 27, 2, 55, 44, tzinfo=tzutc())}
                }
            }
        }
    })


def test_changed(changes):
    assert_matches(changes['playback']['changed'], [
        ('imdb', 'tt0496424'),
        ('tmdb', '4608'),
        ('tvdb', '79488'),
        ('tvrage', '11215')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    3: {
                        'progress': (
                            0.65,
                            6.65
                        ),
                        'paused_at': (
                            datetime.datetime(2015, 3, 7, 1, 24, 15, tzinfo=tzutc()),
                            datetime.datetime(2015, 3, 7, 1, 24, 15, tzinfo=tzutc())
                        )
                    }
                }
            }
        }
    })

    assert_matches(changes['playback']['changed'], [
        ('imdb', 'tt0934814'),
        ('tmdb', '1404'),
        ('tvdb', '80348'),
        ('tvrage', '15614')
    ], {
        'seasons': {
            1: {
                'episodes': {
                    2: {
                        'progress': (
                            7.49,
                            1.19
                        ),
                        'paused_at': (
                            datetime.datetime(2015, 4, 12, 5, 53, 48, tzinfo=tzutc()),
                            datetime.datetime(2015, 4, 12, 5, 53, 48, tzinfo=tzutc())
                        )
                    }
                }
            }
        }
    })


def test_removed(changes):
    assert_matches(changes['playback']['removed'], [
        ('imdb', 'tt1800864'),
        ('tmdb', '34634'),
        ('tvdb', '208111'),
        ('tvrage', '26961')
    ], {
        'seasons': {
            0: {
                'episodes': {
                    1: {'progress': 23.0, 'paused_at': datetime.datetime(2015, 3, 20, 23, 24, 5, tzinfo=tzutc())}
                }
            }
        }
    })

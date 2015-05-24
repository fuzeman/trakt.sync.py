from tests.differ.core.helpers import load

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

    return differ.run(base, current)


def test_watched(changes):
    # Ensure changes are detected properly
    assert changes['watched'] == {
        'removed': {
            ('tvdb', '84912'): {
                'seasons': {
                    6: {
                        'episodes': {
                            1: {'last_watched_at': datetime.datetime(2014, 4, 14, 8, 4, 13), 'plays': 1}
                        }
                    }
                }
            },
            ('tvdb', '79488'): {
                'seasons': {
                    1: {
                        'episodes': {
                            1: {'last_watched_at': datetime.datetime(2015, 1, 26, 5, 37, 3), 'plays': 1},
                            2: {'last_watched_at': datetime.datetime(2015, 2, 24, 0, 50, 41), 'plays': 1},
                            3: {'last_watched_at': datetime.datetime(2015, 2, 28, 1, 16, 26), 'plays': 1}
                        }
                    }
                }
            }
        },
        'added': {
            ('tvdb', '84912'): {
                'seasons': {
                    5: {
                        'episodes': {
                            2: {'last_watched_at': datetime.datetime(2015, 1, 28, 20, 26, 15), 'plays': 3}
                        }
                    }
                }
            },
            ('tvdb', '80348'): {
                'seasons': {
                    1: {
                        'episodes': {
                            2: {'last_watched_at': datetime.datetime(2015, 3, 10, 5, 21, 51), 'plays': 9},
                            4: {'last_watched_at': datetime.datetime(2015, 1, 29, 11, 29, 50), 'plays': 1}
                        }
                    }
                }
            }
        }
    }


def test_collection(changes):
    # Ensure changes are detected properly
    assert changes['collection'] == {
        'removed': {
            ('tvdb', '260750'): {
                'seasons': {
                    2: {
                        'episodes': {
                            2: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52)}
                        }
                    },
                    3: {
                        'episodes': {
                            1: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52)},
                            2: {'collected_at': datetime.datetime(2015, 2, 8, 3, 51, 52)}
                        }
                    }
                }
            }
        },
        'added': {
            ('tvdb', '84912'): {
                'seasons': {
                    6: {
                        'episodes': {
                            2: {'collected_at': datetime.datetime(2014, 2, 15, 5, 35, 30)}
                        }
                    }
                }
            },
            ('tvdb', '208111'): {
                'seasons': {
                    0: {
                        'episodes': {
                            1: {'collected_at': datetime.datetime(2014, 9, 15, 1, 50)}
                        }
                    }
                }
            },
            ('tvdb', '79488'): {
                'seasons': {
                    1: {
                        'episodes': {
                            2: {'collected_at': datetime.datetime(2013, 10, 11, 7, 41, 56)}
                        }
                    }
                }
            },
            ('tvdb', '270633'): {
                'seasons': {
                    1: {
                        'episodes': {
                            1: {'collected_at': datetime.datetime(2014, 1, 29, 12, 56, 35)}
                        }
                    }
                }
            }
        }
    }


def test_rating(changes):
    # Ensure changes are detected properly
    assert changes['rating'] == {
        'removed': {
            ('tvdb', '80348'): {
                'seasons': {
                    1: {
                        'episodes': {
                            1: {'rating': trakt.objects.Rating(10, datetime.datetime(2014, 10, 19, 23, 2, 24))}
                        }
                    }
                }
            },
            ('tvdb', '270633'): {
                'rating': trakt.objects.Rating(6, datetime.datetime(2014, 5, 10, 0, 23, 37))
            }
        },
        'added': {
            ('tvdb', '73244'): {
                'seasons': {
                    4: {
                        'episodes': {
                            2: {'rating': trakt.objects.Rating(10, datetime.datetime(2015, 1, 7, 8, 31, 54))}
                        }
                    }
                }
            },
            ('tvdb', '79488'): {
                'rating': trakt.objects.Rating(8, datetime.datetime(2014, 10, 19, 23, 2, 23))
            }
        },
        'changed': {
            ('tvdb', '110381'): {
                'seasons': {
                    3: {
                        'episodes': {
                            1: {'rating': (
                                trakt.objects.Rating(8, datetime.datetime(2015, 1, 17, 4, 35, 22)),
                                trakt.objects.Rating(6, datetime.datetime(2015, 1, 17, 4, 35, 22))
                            )}
                        }
                    }
                }
            },
            ('tvdb', '73244'): {
                'rating': (
                    trakt.objects.Rating(10, datetime.datetime(2014, 11, 1, 0, 26, 18)),
                    trakt.objects.Rating(8, datetime.datetime(2014, 11, 1, 0, 26, 18))
                ),
                'seasons': {
                    4: {
                        'episodes': {
                            1: {'rating': (
                                trakt.objects.Rating(10, datetime.datetime(2015, 1, 7, 8, 31, 54)),
                                trakt.objects.Rating(8, datetime.datetime(2015, 1, 7, 8, 31, 54))
                            )}
                        }
                    }
                }
            },
            ('tvdb', '80348'): {
                'rating': (
                    trakt.objects.Rating(8, datetime.datetime(2014, 10, 19, 23, 2, 23)),
                    trakt.objects.Rating(10, datetime.datetime(2014, 10, 19, 23, 2, 23))
                )
            }
        }
    }


def test_playback(changes):
    # Ensure changes are detected properly
    assert changes['playback'] == {
        'removed': {
            ('tvdb', '208111'): {
                'seasons': {
                    0: {
                        'episodes': {
                            1: {'progress': 23.0, 'paused_at': datetime.datetime(2015, 3, 20, 23, 24, 5)}
                        }
                    }
                }
            }
        },
        'added': {
            ('tvdb', '260750'): {
                'seasons': {
                    2: {
                        'episodes': {
                            1: {'progress': 0.68, 'paused_at': datetime.datetime(2015, 3, 27, 2, 55, 44)}
                        }
                    }
                }
            }
        },
        'changed': {
            ('tvdb', '79488'): {
                'seasons': {
                    1: {
                        'episodes': {
                            3: {
                                'progress': (
                                    0.65,
                                    6.65
                                ),
                                'paused_at': (
                                    datetime.datetime(2015, 3, 7, 1, 24, 15),
                                    datetime.datetime(2015, 3, 7, 1, 24, 15)
                                )
                            }
                        }
                    }
                }
            },
            ('tvdb', '80348'): {
                'seasons': {
                    1: {
                        'episodes': {
                            2: {
                                'progress': (
                                    7.49,
                                    1.19
                                ),
                                'paused_at': (
                                    datetime.datetime(2015, 4, 12, 5, 53, 48),
                                    datetime.datetime(2015, 4, 12, 5, 53, 48)
                                )
                            }
                        }
                    }
                }
            }
        }
    }

try:
    from trakt_sync.cache.backends.klepto_ import KleptoBackend
except ImportError, ex:
    KleptoBackend = None

    print 'Unable to import "KleptoBackend" - %s', ex

__all__ = ['KleptoBackend']

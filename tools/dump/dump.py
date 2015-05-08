from trakt import Trakt
import os
import requests


def authenticate():
    access_token = os.environ.get('ACCESS_TOKEN')

    if access_token:
        return access_token

    print 'Navigate to %s' % Trakt['oauth'].pin_url()
    pin = raw_input('Pin: ')

    authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
    access_token = authorization.get('access_token')

    print "Access Token: %r" % access_token
    return access_token


def dump_collection(headers, collection, media):
    print "dump_collection - collection: %r, media: %r" % (collection, media)

    # Fetch collection
    response = requests.get('https://api-v2launch.trakt.tv/sync/%s/%s' % (collection, media), headers=headers)

    # Ensure directory exists
    directory = 'out/%s' % collection

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write data to file
    with open('%s/%s.json' % (directory, media), 'wb') as fp:
        fp.write(response.content)


if __name__ == '__main__':
    Trakt.configuration.defaults.app(
        id=os.environ.get('APP_ID')
    )

    Trakt.configuration.defaults.client(
        id=os.environ.get('CLIENT_ID'),
        secret=os.environ.get('CLIENT_SECRET')
    )

    access_token = authenticate()

    headers = {
        'Authorization': 'Bearer ' + access_token,

        'trakt-api-version': 2,
        'trakt-api-key': os.environ.get('CLIENT_ID')
    }

    raw_input('[dump]')

    # Movies
    dump_collection(headers, 'collection', 'movies')
    dump_collection(headers, 'playback', 'movies')
    dump_collection(headers, 'ratings', 'movies')
    dump_collection(headers, 'watched', 'movies')

    # Shows/Episodes
    dump_collection(headers, 'collection', 'shows')
    dump_collection(headers, 'playback', 'episodes')
    dump_collection(headers, 'ratings', 'shows')
    dump_collection(headers, 'ratings', 'episodes')
    dump_collection(headers, 'watched', 'shows')

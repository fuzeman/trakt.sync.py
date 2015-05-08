import json
import os

TESTS_DIR = os.path.abspath(os.path.dirname(__file__) + '\\..')
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')


def read(path):
    with open(get_fixture_path(path), 'rb') as fp:
        return fp.read()


def read_json(path):
    with open(get_fixture_path(path), 'rb') as fp:
        return json.load(fp)


def get_fixture_path(path):
    return os.path.join(FIXTURES_DIR, path)

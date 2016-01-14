from trakt_sync import __version__

from setuptools import setup, find_packages

setup(
    name='trakt.sync.py',
    version=__version__,
    license='MIT',
    url='https://github.com/fuzeman/trakt.sync.py',

    author='Dean Gardiner',
    author_email='me@dgardiner.net',

    description='Sync extension for trakt.py',
    packages=find_packages(exclude=[
        'examples'
    ]),
    platforms='any',

    install_requires=[
        'trakt.py',
        'pyemitter'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)

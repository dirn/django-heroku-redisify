# -*- coding: utf-8 -*-

""" Friendly Redis for Django on Heroku """

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

urlparse.uses_netloc.append('redis')

REDIS_URLS = (
    'REDISTOGO_URL',
    'OPENREDIS_URL',
    'REDISGREEN_URL',
    'MYREDIS_URL',
    'REDISCLOUD_URL',
)


def redisify(default=None, db=0):
    """Returns configured CACHES dictionary based on environment settings.

    :param default: A URL for a Redis database.
    :type default: str.
    :param db: The db to use
    :type default: int.
    :returns: dict -- A configured dictionary that can be used for
              django.conf.settings.CACHES.

    Supported providers:

    - Redis To Go (REDISTOGO_URL)
    - openredis (OPENREDIS_URL)
    - RedisGreen (REDISGREEN_URL)
    - MyRedis (MYREDIS_URL)
    - RedisCloud (REDISCLOUD_URL)

    Other Redis hosts can be utilized by passing the URL as ``default``::

        redisify(default='redis://localhost')

    .. versionchanged:: 0.2.0
       Added support for openredis
    """
    url = None
    # If any of the supported URL environment variables exist, use the first
    # one defined in `REDIS_URLS`.
    urls = (os.getenv(url) for url in REDIS_URLS if os.getenv(url))
    for url in urls:
        break

    # If no supported URLs exist and a default is provided, use it.
    if not url and default is not None:
        url = default

    if url is not None:
        # Parse the URL and build the configured dictionary. All settings are
        # based on those recommended by Heroku.
        url = _parse(url)
        return dict(
            BACKEND='redis_cache.RedisCache',
            LOCATION='{0}{1}'.format(url['HOST'],
                ':{0}'.format(url['PORT']) if url['PORT'] is not None else ''),
            OPTIONS=dict(
                DB=db,
                PARSER_CLASS='redis.connection.HiredisParser',
                PASSWORD=url['PASSWORD'],
            )
        )


def _parse(url):
    """Returns a dictionary of a parsed URL."""
    url = urlparse.urlparse(url)

    return dict(
        HOST=url.hostname,
        USER=url.username,
        PASSWORD=url.password,
        PORT=url.port,
    )

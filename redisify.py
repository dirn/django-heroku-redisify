# -*- coding: utf-8 -*-

""" Friendly Redis for Django on Heroku """

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

__all__ = ('redisify')

urlparse.uses_netloc.append('redis')

REDIS_URLS = (
    'REDISTOGO_URL',
    'OPENREDIS_URL',
    'REDISGREEN_URL',
    'MYREDIS_URL',
    'REDISCLOUD_URL',
)


def redisify(default=None):
    """Returns configured CACHES dictionary based on environment settings.

    This method will look for Redis URLs in the environment settings. It
    will first check for ``REDIS_URL``. If this setting is found, it
    will be in the result ``dict`` as the ``default`` key. The method
    will then iterate through the settings looking for any additional
    Redis URLs. Any that are found will be added to the result ``dict``.

    In the event that ``REDIS_URL`` was not found, the first Redis URL
    encountered will be used as the ``default`` key. This URL will
    appear twice.

    In the event that ``REDIS_URL`` was not found and no other Redis
    URLs were found, the value provided through the ``default`` argument
    will be used as the ``default`` key.

    If ``default`` was no provided and no other Redis URLs were found,
    the ``dict`` will be empty.

    :param default: A URL for a Redis database.
    :type default: str.
    :returns: dict -- A configured dictionary that can be used for
              django.conf.settings.CACHES.

    .. versionchanged:: 0.3.0
       ``redisify()`` now returns a ``dict`` containing all caches
    .. versionadded:: 0.1.0
    """

    urls = {}

    if 'REDIS_URL' in os.environ:
        urls['default'] = os.environ['REDIS_URL']

    for k, v in os.environ.items():
        if not v.startswith('redis://') or k == 'REDIS_URL':
            continue

        key = k.split('_')
        if 'URI' in key:
            key.remove('URI')
        if 'URL' in key:
            key.remove('URL')
        key = '_'.join(key)

        urls[key] = v

        if 'default' not in urls:
            urls['default'] = v

    if not ('default' in urls or default is None):
        urls['default'] = default

    caches = {}

    for k, v in urls.items():
        url = _parse(v)

        caches[k] = {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '{0}:{1}'.format(url['HOST'], url['PORT']),
            'OPTIONS': {
                'DB': url['DB'],
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'PASSWORD': url['PASSWORD'],
            },
        }

    return caches


def _parse(url):
    """Returns a dictionary of a parsed URL."""
    url = urlparse.urlparse(url)

    return {
        'HOST': url.hostname,
        'USERNAME': url.username,
        'PASSWORD': url.password,
        'PORT': int(url.port) if url.port else 6379,
        'DB': int(url.path[1:]) if url.path[1:] else 0,
    }

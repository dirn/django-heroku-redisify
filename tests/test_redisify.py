#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os

from redisify import redisify, _parse


class RedisifyTest(unittest.TestCase):
    def setUp(self):
        os.environ.pop('REDIS_URL', None)
        os.environ.pop('OTHER_REDIS_URL', None)
        os.environ.pop('ANOTHER_REDIS_URI', None)

    def test_all(self):
        """Test all settings"""

        os.environ['REDIS_URL'] = 'redis://localhost/1'
        os.environ['OTHER_REDIS_URL'] = 'redis://localhost/2'

        caches = redisify(default='redis://localhost')

        self.assertEqual(caches['default']['LOCATION'], 'localhost:6379')
        self.assertEqual(caches['OTHER_REDIS']['LOCATION'], 'localhost:6379')

        self.assertEqual(caches['default']['OPTIONS']['DB'], 1)
        self.assertEqual(caches['OTHER_REDIS']['OPTIONS']['DB'], 2)

    def test_default(self):
        """Test passing a default value"""

        caches = redisify(default='redis://localhost')

        self.assertEqual(caches['default']['LOCATION'], 'localhost:6379')
        self.assertEqual(caches['default']['OPTIONS']['DB'], 0)

    def test_none(self):
        """Test no values at all"""

        caches = redisify()

        self.assertEqual(caches, {})

    def test_others(self):
        """Test other environment settings"""

        os.environ['OTHER_REDIS_URL'] = 'redis://localhost/1'
        os.environ['ANOTHER_REDIS_URI'] = 'redis://localhost/2'

        caches = redisify()

        self.assertTrue('default' in caches)

        self.assertTrue(caches['default'] == caches['OTHER_REDIS'] or
                        caches['default'] == caches['ANOTHER_REDIS'])

        self.assertEqual(caches['OTHER_REDIS']['LOCATION'], 'localhost:6379')
        self.assertEqual(caches['ANOTHER_REDIS']['LOCATION'], 'localhost:6379')

        self.assertEqual(caches['OTHER_REDIS']['OPTIONS']['DB'], 1)
        self.assertEqual(caches['ANOTHER_REDIS']['OPTIONS']['DB'], 2)

    def test_redis_url(self):
        """Test `REDIS_URL` setting"""

        os.environ['REDIS_URL'] = 'redis://localhost/1'

        caches = redisify(default='redis://localhost')

        self.assertEqual(caches['default']['LOCATION'], 'localhost:6379')
        self.assertEqual(caches['default']['OPTIONS']['DB'], 1)

    def test_settings(self):
        """Test settings.CACHES"""

        caches = redisify(default='redis://username:password@hostname:1234/5')

        self.assertEqual(caches['default']['BACKEND'], 'redis_cache.RedisCache')
        self.assertEqual(caches['default']['LOCATION'], 'hostname:1234')

        self.assertEqual(caches['default']['OPTIONS']['DB'], 5)
        self.assertEqual(caches['default']['OPTIONS']['PARSER_CLASS'],
                         'redis.connection.HiredisParser')
        self.assertEqual(caches['default']['OPTIONS']['PASSWORD'], 'password')

    def test__parse(self):
        """Test the `_parse()` method"""

        parsed = _parse('redis://username:password@hostname.com:1234/5')

        self.assertEqual(parsed['HOST'], 'hostname.com')
        self.assertEqual(parsed['USERNAME'], 'username')
        self.assertEqual(parsed['PASSWORD'], 'password')
        self.assertEqual(parsed['PORT'], 1234)
        self.assertEqual(parsed['DB'], 5)

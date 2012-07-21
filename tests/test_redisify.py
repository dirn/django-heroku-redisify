#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os
import sys

from redisify import redisify, _parse

sys.path.insert(0, os.path.abspath('..'))
sys.path.append('.')


class RedisifyTest(unittest.TestCase):
    def setUp(self):
        # URL for localhost
        self.localhost = 'redis://localhost'
        # URL for Redis To Go
        self.redistogo = \
            'redis://redistogo:password@example.redistogo.com:6379'

    def test__parse_localhost(self):
        """Test the internal parser with localhost"""
        parsed = _parse(self.localhost)

        self.assertEqual(parsed['HOST'], 'localhost')
        self.assertTrue(parsed['USER'] is None)
        self.assertTrue(parsed['PASSWORD'] is None)
        self.assertTrue(parsed['PORT'] is None)

    def test__parse_redistogo(self):
        """Test the internal parser with REDISTOGO_URL"""
        parsed = _parse(self.redistogo)

        self.assertEqual(parsed['HOST'], 'example.redistogo.com')
        self.assertEqual(parsed['USER'], 'redistogo')
        self.assertEqual(parsed['PASSWORD'], 'password')
        self.assertEqual(parsed['PORT'], 6379)

    def test_backend(self):
        """Test the BACKEND setting"""
        caches = redisify(default=self.localhost)

        self.assertEqual(caches['BACKEND'], 'redis_cache.RedisCache')

    def test_default(self):
        """Test passing a default value"""
        caches = redisify(default=self.localhost)

        self.assertEqual(caches['LOCATION'], 'localhost')
        self.assertTrue(caches['OPTIONS']['PASSWORD'] is None)

    def test_no_default(self):
        """Test passing no default value"""
        caches = redisify()

        self.assertTrue(caches is None)

    def test_parser_class(self):
        """Test the PARSER_CLASS setting"""
        caches = redisify(default=self.localhost)

        self.assertEqual(caches['OPTIONS']['PARSER_CLASS'],
            'redis.connection.HiredisParser')

    def test_redistogo(self):
        """Test using REDISTOGO_URL"""
        if 'REDISTOGO_URL' in os.environ:
            tmp = os.environ['REDISTOGO_URL']
        else:
            tmp = None

        os.environ['REDISTOGO_URL'] = self.redistogo

        caches = redisify()

        # Make sure to clean up the setting
        if tmp is None:
            del os.environ['REDISTOGO_URL']
        else:
            os.environ['REDISTOGO_URL'] = tmp

        self.assertEqual(caches['LOCATION'], 'example.redistogo.com:6379')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password')

if __name__ == '__main__':
    unittest.main()

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
        # URL for MyRedis
        self.myredis = \
            'redis://myredis:abcdef123456@example.ec2.myredis.com:6123/'
        # URL for openredis
        self.openredis = \
            'redis://openredis:password2@example.openredis.com:63792'
        # URL for RedisGreen
        self.redisgreen = \
            'redis://rg:gnysfn55t65g72ntd4g0a6h8ea91ca9v@' \
            'smart-panda.redisgreen.net:10030'
        # URL for Redis To Go
        self.redistogo = \
            'redis://redistogo:password@example.redistogo.com:6379'

        # If the provider URLs already exist in the environment,
        # back them up and delete them.
        if 'MYREDIS_URL' in os.environ:
            self.MYREDIS_URL = os.environ['MYREDIS_URL']
            del os.environ['MYREDIS_URL']
        else:
            self.MYREDIS_URL = None
        if 'OPENREDIS_URL' in os.environ:
            self.OPENREDIS_URL = os.environ['OPENREDIS_URL']
            del os.environ['OPENREDIS_URL']
        else:
            self.OPENREDIS_URL = None
        if 'REDISGREEN_URL' in os.environ:
            self.REDISGREEN_URL = os.environ['REDISGREEN_URL']
            del os.environ['REDISGREEN_URL']
        else:
            self.REDISGREEN_URL = None
        if 'REDISTOGO_URL' in os.environ:
            self.REDISTOGO_URL = os.environ['REDISTOGO_URL']
            del os.environ['REDISTOGO_URL']
        else:
            self.REDISTOGO_URL = None

    def tearDown(self):
        # Restore any provider URLs to the environment or remove any
        # temporary ones left over from testing.
        if self.MYREDIS_URL is not None:
            os.environ['MYREDIS_URL'] = self.MYREDIS_URL
        elif 'MYREDIS_URL' in os.environ:
            del os.environ['MYREDIS_URL']
        if self.OPENREDIS_URL is not None:
            os.environ['OPENREDIS_URL'] = self.OPENREDIS_URL
        elif 'OPENREDIS_URL' in os.environ:
            del os.environ['OPENREDIS_URL']
        if self.REDISGREEN_URL is not None:
            os.environ['REDISGREEN_URL'] = self.REDISGREEN_URL
        elif 'REDISGREEN_URL' in os.environ:
            del os.environ['REDISGREEN_URL']
        if self.REDISTOGO_URL is not None:
            os.environ['REDISTOGO_URL'] = self.REDISTOGO_URL
        elif 'REDISTOGO_URL' in os.environ:
            del os.environ['REDISTOGO_URL']

    def test__parse_localhost(self):
        """Test the internal parser with localhost"""
        parsed = _parse(self.localhost)

        self.assertEqual(parsed['HOST'], 'localhost')
        self.assertTrue(parsed['USER'] is None)
        self.assertTrue(parsed['PASSWORD'] is None)
        self.assertTrue(parsed['PORT'] is None)

    def test__parse_myredis(self):
        """Test the internal parser with MYREDIS_URL"""
        parsed = _parse(self.myredis)

        self.assertEqual(parsed['HOST'], 'example.ec2.myredis.com')
        self.assertEqual(parsed['USER'], 'myredis')
        self.assertEqual(parsed['PASSWORD'], 'abcdef123456')
        self.assertEqual(parsed['PORT'], 6123)

    def test__parse_openredis(self):
        """Test the internal parser with OPENREDIS_URL"""
        parsed = _parse(self.openredis)

        self.assertEqual(parsed['HOST'], 'example.openredis.com')
        self.assertEqual(parsed['USER'], 'openredis')
        self.assertEqual(parsed['PASSWORD'], 'password2')
        self.assertEqual(parsed['PORT'], 63792)

    def test__parse_redisgreen(self):
        """Test the internal parser with REDISGREEN_URL"""
        parsed = _parse(self.redisgreen)

        self.assertEqual(parsed['HOST'], 'smart-panda.redisgreen.net')
        self.assertEqual(parsed['USER'], 'rg')
        self.assertEqual(parsed['PASSWORD'], 'gnysfn55t65g72ntd4g0a6h8ea91ca9v')
        self.assertEqual(parsed['PORT'], 10030)

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

    def test_myredis(self):
        """Test using MYREDIS_URL"""
        os.environ['MYREDIS_URL'] = self.myredis

        caches = redisify()

        self.assertEqual(caches['LOCATION'], 'example.ec2.myredis.com:6123')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'abcdef123456')

    def test_myredis_trumps_default(self):
        """Test using MYREDIS_URL with a default"""
        os.environ['MYREDIS_URL'] = self.myredis

        caches = redisify(default=self.localhost)

        self.assertEqual(caches['LOCATION'], 'example.ec2.myredis.com:6123')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'abcdef123456')

    def test_openredis(self):
        """Test using OPENREDIS_URL"""
        os.environ['OPENREDIS_URL'] = self.openredis

        caches = redisify()

        self.assertEqual(caches['LOCATION'], 'example.openredis.com:63792')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password2')

    def test_openredis_trumps_default(self):
        """Test using OPENREDIS_URL with a default"""
        os.environ['OPENREDIS_URL'] = self.openredis

        caches = redisify(default=self.localhost)

        self.assertEqual(caches['LOCATION'], 'example.openredis.com:63792')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password2')

    def test_parser_class(self):
        """Test the PARSER_CLASS setting"""
        caches = redisify(default=self.localhost)

        self.assertEqual(caches['OPTIONS']['PARSER_CLASS'],
            'redis.connection.HiredisParser')

    def test_redisgreen(self):
        """Test using REDISGREEN_URL"""
        os.environ['REDISGREEN_URL'] = self.redisgreen

        caches = redisify()

        self.assertEqual(caches['LOCATION'],
                         'smart-panda.redisgreen.net:10030')
        self.assertEqual(caches['OPTIONS']['PASSWORD'],
                         'gnysfn55t65g72ntd4g0a6h8ea91ca9v')

    def test_redisgreen_trumps_default(self):
        """Test using REDISGREEN_URL with a default"""
        os.environ['REDISGREEN_URL'] = self.redisgreen

        caches = redisify(default=self.localhost)

        self.assertEqual(caches['LOCATION'],
                         'smart-panda.redisgreen.net:10030')
        self.assertEqual(caches['OPTIONS']['PASSWORD'],
                         'gnysfn55t65g72ntd4g0a6h8ea91ca9v')

    def test_redistogo(self):
        """Test using REDISTOGO_URL"""
        os.environ['REDISTOGO_URL'] = self.redistogo

        caches = redisify()

        self.assertEqual(caches['LOCATION'], 'example.redistogo.com:6379')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password')

    def test_redistogo_trumps_all(self):
        """Test with all possibilities set"""
        os.environ['REDISTOGO_URL'] = self.redistogo
        os.environ['OPENREDIS_URL'] = self.openredis
        os.environ['REDISGREEN_URL'] = self.redisgreen
        os.environ['MYREDIS_URL'] = self.myredis

        caches = redisify()

        self.assertEqual(caches['LOCATION'], 'example.redistogo.com:6379')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password')

    def test_redistogo_trumps_default(self):
        """Test using REDISTOGO_URL with a default"""
        os.environ['REDISTOGO_URL'] = self.redistogo

        caches = redisify(default=self.localhost)

        self.assertEqual(caches['LOCATION'], 'example.redistogo.com:6379')
        self.assertEqual(caches['OPTIONS']['PASSWORD'], 'password')

if __name__ == '__main__':
    unittest.main()

===========================================================
django-heroku-redisify: Friendly Redis for Django on Heroku
===========================================================

.. image:: https://secure.travis-ci.org/dirn/django-heroku-redisify.png?branch=master

A user-friendly method to configure Django projects on Heroku to use Redis.

Inspired by the work of `Randall Degges`_.

.. _Randall Degges: https://github.com/rdegges


Usage
=====

Place this code into your project's settings.py::

    from redisify import redisify
    CACHES = redisify(default='redis://localhost')

Full documentation can be found on `Read the Docs`_.

.. _Read the Docs: http://readthedocs.org/docs/django-heroku-redisify/en/latest/


Installation
============

To install the latest version of django-heroku-redisify::

    $ pip install django-heroku-redisify

or, if you must::

    $ easy_install django-heroku-redisify

To install the latest development version::

    $ git clone git@github.com:dirn/django-heroku-redisify.git
    $ cd django-heroku-redisify
    $ python setup.py install


Changelog
=========

- 0.2.0
  - THIS RELEASE IS NOT BACKWARDS COMPATIBLE
  - ``redisify()`` now returns a ``dict`` of all URLs found in the
  environment settings.

- 0.1.0
  - Initial release

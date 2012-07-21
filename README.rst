===========================================================
django-heroku-redisify: Friendly Redis for Django on Heroku
===========================================================

A user-friendly method to configure Django projects on Heroku to use Redis.

Inspired by the work of `Randall Degges`_.

.. _Randall Degges: https://github.com/rdegges

Usage
=====

Place this code into your project's settings.py::

    from redisify import redisify
    CACHES = {'default': redisify(default='redis://localhost')}

Full documentation can be found on `Read the Docs`_.

.. _Read the Docs: http://readthedocs.org/docs/django-heroku-redisify/en/latest/

Installation
============

Installing django-heroku-redisify is easy::

    pip install django-heroku-redisify

or download the source and run::

    python setup.py install

django-heroku-redisify 0.1.0
===================================

.. image:: https://secure.travis-ci.org/dirn/django-heroku-redisify.png?branch=master

django-heroku-redisify provides a user-friendly method to configure Django
projects on Heroku to use Redis.

Inspired by the work of `Randall Degges`_.

.. _Randall Degges: https://github.com/rdegges

.. toctree::
   :maxdepth: 2

Usage
-----

In settings.py::

    from redisify import redisify
    CACHES = {'default': redisify(default='redis://localhost')}

.. automodule:: redisify
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


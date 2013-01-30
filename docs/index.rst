======================
django-heroku-redisify
======================

django-heroku-redisify provides a user-friendly method to configure Django
projects on Heroku to use Redis.

Inspired by the work of `Randall Degges`_.

.. _Randall Degges: https://github.com/rdegges

.. toctree::
   :maxdepth: 2


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


Usage
=====

In settings.py::

    from redisify import redisify
    CACHES = redisify(default='redis://localhost')


API
===

.. automodule:: redisify
   :members:


Changelog
=========

- 0.2.0
  - THIS RELEASE IS NOT BACKWARDS COMPATIBLE
  - ``redisify()`` now returns a ``dict`` of all URLs found in the
  environment settings.

- 0.1.0
  - Initial release


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


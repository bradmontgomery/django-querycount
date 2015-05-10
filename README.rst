forked from Django Querycount
=================
add SQL statistic ignore pattern support. 

|version| |license|

Inspired by `this post by David Szotten <http://goo.gl/UUKN0r>`_, this project
gives you a middleware that prints DB query counts in Django's runserver
console output.

|screenshot|


Installation
------------

    pip install django-querycount

Just add ``querycount.middleware.QueryCountMiddleware`` to your
``MIDDLEWARE_CLASSES``.

Notice that django-querycount is hard coded to work only in DEBUG mode set to true

Settings
--------

There are two possible settings for this app: The first defines threshold
values used to color output, while the second allows you customize requests
that will be ignored by the middleware.  The default settings are::

    QUERYCOUNT {
        'THRESHOLDS': {
            'MEDIUM': 50,
            'HIGH': 200,
            'MIN_TIME_TO_LOG':0,
            'MIN_QUERY_COUNT_TO_LOG':0
        },
        'IGNORE_PATTERNS': [],
    }


The ``QUERYCOUNT['THRESHOLDS']`` settings will determine how many queries are
interpreted as high or medium (and the color-coded output). In previous versions
of this app, this settings was called ``QUERYCOUNT_THRESHOLDS`` and that setting
is still supported.

The ``QUERYCOUT['IGNORE_PATTERNS']`` setting allows you to define a list of
regexp patterns that get applied to each request's path. If there is a match,
the middleware will not be applied to that request. For example, the following
setting would bypass the querycount middleware for all requests to the admin::

    QUERYCOUNT = {
        'IGNORE_PATTERNS': [r'^/admin/']
    }


License
-------

This code is distributed under the terms of the MIT license.

Testing
-------

Works only in context of a django installation venv: cd querycount/tests && python test.py


.. |version| image:: http://img.shields.io/pypi/v/django-querycount.svg?style=flat-square
    :alt: Current Release
    :target: https://pypi.python.org/pypi/django-querycount/

.. |license| image:: http://img.shields.io/pypi/l/django-querycount.svg?style=flat-square
    :alt: License
    :target: https://pypi.python.org/pypi/django-querycount/

.. |screenshot| image:: screenshot.png
    :alt: django-querycount in action

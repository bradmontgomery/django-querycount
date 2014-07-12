Django Querycount
=================

Inspired by `this post by David Szotten <http://goo.gl/UUKN0r>`_, this project
gives you a middleware that prints DB query counts in Django's runserver
console output.


Installation
------------

Add ``querycount`` to your ``INSTALLED_APPS``, then add
``querycount.middleware.QueryCountMiddleware`` do your ``MIDDLEWARE_CLASSES``.


License
-------

This code is distributed under the terms of the MIT license.

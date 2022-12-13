# Testing

Run `python manage.py test querycount` to run the tests. Note that this will
modify your settings so that your project is in DEBUG mode for the duration
of the `querycount` tests.

**Warning**: this project needs better tests; for the moment, there are only
smoke tests that set up the middleware and call two simple test views.

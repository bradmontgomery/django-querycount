from django.test import TestCase, modify_settings, override_settings
from querycount.middleware import QueryCountMiddleware


DEFAULT_QC_SETTINGS = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}

QC_MIDDLEWARE = {
    'append': 'querycount.middleware.QueryCountMiddleware',
}


@modify_settings(MIDDLEWARE=QC_MIDDLEWARE)
@override_settings(QUERYCOUNT=DEFAULT_QC_SETTINGS)
@override_settings(ROOT_URLCONF='querycount.tests.urls')
@override_settings(DEBUG=True)
class QueryCountTestCase(TestCase):
    # -------------------------------------------------------------------------
    # TODO: I want this app to be testable with just django's built-in tools,
    #       e.g. by running `python manage.py test querycount`.
    #
    #   - Figure out if there's a way to access the Middleware classes from a
    #     test client?
    #   - How to generate DB queries (read + write) reliably without jumping
    #     through the hoops of having a `test app` (that then needs to be
    #     monkey-patched in)
    #   - Should we just write a dump unit test for each of the
    #     QueryCountMiddleware's methods (probably).
    # -------------------------------------------------------------------------

    def setUp(self):
        self.querycount = QueryCountMiddleware()

    def test_empty(self):
        # Smoke test for a view that does no DB queries.
        resp = self.client.get("/empty/")
        self.assertEqual(resp.status_code, 200)

    def test_count(self):
        # Smoke test for a view that does a single DB queries.
        resp = self.client.get("/count/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(resp['X-DjangoQueryCount-Count']), 1)

    def test_header_disabled(self):
        # Ensure removing the count header is effective
        disabled_settings = DEFAULT_QC_SETTINGS
        disabled_settings['RESPONSE_HEADER'] = None

        with self.settings(QUERYCOUNT=disabled_settings):
            resp = self.client.get("/count/")            
            self.assertEqual(resp.status_code, 200)
            self.assertFalse('X-DjangoQueryCount-Count' in resp)

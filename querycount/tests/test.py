#!/usr/bin/env python

from __future__ import absolute_import

import os
import sys

from test_app.settings import DEFAULT_SETTINGS

from django.conf import settings

if settings.configured is not True:
    settings.configure(**DEFAULT_SETTINGS)
settings.DEBUG = True

from django.test import TestCase

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from middleware import QueryCountMiddleware
from test_app.models import TestModel


class QueryCountTestCase(TestCase):

        def setUp(self):
            self.querycount = QueryCountMiddleware()

        def test_setup(self):
            for name, details in DEFAULT_SETTINGS['DATABASES'].items():
                self.assertTrue(settings.DEBUG)
                self.assertIn(name, self.querycount.dbs)

        def get_fresh_stats(self):
            self.querycount._reset_stats()
            for key in self.querycount.stats.keys():
                self.querycount._count_queries(key)
            return self.querycount.stats

        def test_query_stats(self):
            starting_stats = self.get_fresh_stats()

            # ensure that writes are adding correctly
            model_instance = TestModel(text_field='abc').save() # NOQA
            post_write_stats = self.get_fresh_stats()
            for name in self.querycount.dbs:
                for key in self.querycount.stats.keys():
                    self.assertEqual(
                        starting_stats[key][name]['writes'] + 1,
                        post_write_stats[key][name]['writes']
                    )
                    self.assertEqual(
                        starting_stats[key][name]['reads'],
                        post_write_stats[key][name]['reads']
                    )

            # ensure that reads are adding correctly
            model_instance = TestModel.objects.get(pk=1) # NOQA
            post_read_stats = self.get_fresh_stats()
            for name in self.querycount.dbs:
                for key in self.querycount.stats.keys():
                    self.assertEqual(
                        post_write_stats[key][name]['reads'] + 1,
                        post_read_stats[key][name]['reads']
                    )
                    self.assertEqual(
                        post_write_stats[key][name]['writes'],
                        post_read_stats[key][name]['writes']
                    )

if __name__ == '__main__':
    from django.test.runner import DiscoverRunner
    test_runner = DiscoverRunner(verbosity=1, interactive=True, failfast=False)
    test_runner.run_tests(['.'])

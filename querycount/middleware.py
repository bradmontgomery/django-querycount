import re
import sys
import timeit

from django.conf import settings
from django.db import connections
from django.utils import termcolors

from . qc_settings import QC_SETTINGS


class QueryCountMiddleware(object):
    """This middleware prints the number of database queries for each http
    request and response. This code is adapted from: http://goo.gl/UUKN0r"""

    def __init__(self, *args, **kwargs):
        if settings.DEBUG:
            self.request_path = None
            self.stats = {"request": {}, "response": {}}
            self.dbs = [c.alias for c in connections.all()]
            self._reset_stats()

            self._start_time = None
            self._end_time = None
            self.host = None  # The HTTP_HOST pulled from the request

            # colorizing methods
            self.white = termcolors.make_style(opts=('bold',), fg='white')
            self.red = termcolors.make_style(opts=('bold',), fg='red')
            self.yellow = termcolors.make_style(opts=('bold',), fg='yellow')
            self.green = termcolors.make_style(fg='green')

            # query type detection regex
            # TODO: make stats classification regex more robust
            self.read_query_regex = re.compile("SELECT .*")
            self.threshold = QC_SETTINGS['THRESHOLDS']
            super(QueryCountMiddleware, self).__init__(*args, **kwargs)

    def _reset_stats(self):
        self.stats = {"request": {}, "response": {}}
        for alias in self.dbs:
            self.stats["request"][alias] = {'writes': 0, 'reads': 0, 'total': 0}
            self.stats["response"][alias] = {'writes': 0, 'reads': 0, 'total': 0}

    def _count_queries(self, which):
        for c in connections.all():
            for q in c.queries:
                if self.read_query_regex.search(q['sql']) is not None:
                    self.stats[which][c.alias]['reads'] += 1
                else:
                    self.stats[which][c.alias]['writes'] += 1
                self.stats[which][c.alias]['total'] += 1

    def _ignore(self, path):
        """Check to see if we should ignore the request."""
        return any([
            re.match(pattern, path) for pattern in QC_SETTINGS['IGNORE_PATTERNS']
        ])

    def process_request(self, request):
        if settings.DEBUG and not self._ignore(request.path):
            self.host = request.META.get('HTTP_HOST', None)
            self.request_path = request.path
            self._start_time = timeit.default_timer()
            self._count_queries("request")

    def process_response(self, request, response):
        if settings.DEBUG and not self._ignore(request.path):
            self.request_path = request.path
            self._end_time = timeit.default_timer()
            self._count_queries("response")
            self.print_num_queries()
            self._reset_stats()
        return response

    def _stats_table(self, which, path='', output=None):
        if output is None:
            if self.host:
                host_string = 'http://{0}{1}'.format(self.host, self.request_path)
            else:
                host_string = self.request_path
            output = self.white('\n{0}\n'.format(host_string))
            output += "|------|-----------|----------|----------|----------|\n"
            output += "| Type | Database  |   Reads  |  Writes  |  Totals  |\n"
            output += "|------|-----------|----------|----------|----------|\n"

        for db, stats in self.stats[which].items():
            if stats['total'] > 0:
                line = "|{w}|{db}|{reads}|{writes}|{total}|\n".format(
                    w=which.upper()[:4].center(6),
                    db=db.center(11),
                    reads=str(stats['reads']).center(10),
                    writes=str(stats['writes']).center(10),
                    total=str(stats['total']).center(10)
                )
                output += self._colorize(line, stats['total'])
            output += "|------|-----------|----------|----------|----------|\n"
        return output

    def _totals(self, which):
        reads = 0
        writes = 0
        for db, stats in self.stats[which].items():
            reads += stats['reads']
            writes += stats['writes']
        return (reads, writes, reads + writes)

    def _colorize(self, output, metric):
        if metric > self.threshold['HIGH']:
            output = self.red(output)
        elif metric > self.threshold['MEDIUM']:
            output = self.yellow(output)
        else:
            output = self.green(output)
        return output

    def print_num_queries(self):
        # Request data
        request_totals = self._totals("request")
        output = self._stats_table("request")

        # Response data
        response_totals = self._totals("response")
        output = self._stats_table("response", output=output)

        # Summary of both
        if self._end_time and self._start_time:
            elapsed = self._end_time - self._start_time
        else:
            elapsed = 0
        count = request_totals[2] + response_totals[2]  # sum total queries
        sum_output = 'Total queries: {0} in {1:.4f}s \n\n'.format(count, elapsed)
        sum_output = self._colorize(sum_output, count)

        # runserver just prints its output to sys.stderr, so we'll do that too.
        if elapsed >= self.threshold['MIN_TIME_TO_LOG'] and count >= self.threshold['MIN_QUERY_COUNT_TO_LOG']:
            sys.stderr.write(output)
            sys.stderr.write(sum_output)

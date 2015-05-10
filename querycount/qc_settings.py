"""
Default querycount settings.

"""

from django.conf import settings


QC_SETTINGS = {
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    }
}

if getattr(settings, 'QUERYCOUNT', False) and 'THRESHOLDS' in settings.QUERYCOUNT:
    QC_SETTINGS['THRESHOLDS'] = settings.QUERYCOUNT['THRESHOLDS']

if getattr(settings, 'QUERYCOUNT', False) and 'IGNORE_REQUEST_PATTERNS' in settings.QUERYCOUNT:
    QC_SETTINGS['IGNORE_REQUEST_PATTERNS'] = settings.QUERYCOUNT['IGNORE_REQUEST_PATTERNS']

if getattr(settings, 'QUERYCOUNT', False) and 'IGNORE_SQL_PATTERNS' in settings.QUERYCOUNT:
    QC_SETTINGS['IGNORE_SQL_PATTERNS'] = settings.QUERYCOUNT['IGNORE_SQL_PATTERNS']

# Support the old-style settings

# Support the old-style settings
if getattr(settings, 'QUERYCOUNT_THRESHOLDS', False):
    QC_SETTINGS['THRESHOLDS'] = settings.QUERYCOUNT_THRESHOLDS

if getattr(settings, 'QUERYCOUNT', False) and 'IGNORE_PATTERNS' in settings.QUERYCOUNT:
    QC_SETTINGS['IGNORE_REQUEST_PATTERNS'] = settings.QUERYCOUNT['IGNORE_PATTERNS']

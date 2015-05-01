"""
Default querycount settings.

"""

from django.conf import settings


QC_SETTINGS = {
    'IGNORE_PATTERNS': [],
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    }
}

if getattr(settings, 'QUERYCOUNT', False) and 'THRESHOLDS' in settings.QUERYCOUNT:
    QC_SETTINGS['THRESHOLDS'] = settings.QUERYCOUNT['THRESHOLDS']

if getattr(settings, 'QUERYCOUNT', False) and 'IGNORE_PATTERNS' in settings.QUERYCOUNT:
    QC_SETTINGS['IGNORE_PATTERNS'] = settings.QUERYCOUNT['IGNORE_PATTERNS']

# Support the old-style settings
if getattr(settings, 'QUERYCOUNT_THRESHOLDS', False):
    QC_SETTINGS['THRESHOLDS'] = settings.QUERYCOUNT_THRESHOLDS

"""
Default querycount settings.

"""

from django.conf import settings
from django.test.signals import setting_changed


QC_SETTINGS = {
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    },
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count',
}

def _process_settings(**kwargs):
    """
    Apply user supplied settings.
    """

    # If we are in this method due to a signal, only reload for our settings
    setting_name = kwargs.get('setting', None) 
    if setting_name is not None and setting_name != 'QUERYCOUNT':
        return

    # Support the old-style settings
    if getattr(settings, 'QUERYCOUNT_THRESHOLDS', False):
        QC_SETTINGS['THRESHOLDS'] = settings.QUERYCOUNT_THRESHOLDS

    # Apply new-style settings
    if not getattr(settings, 'QUERYCOUNT', False):
        return

    # Duplicate display is a special case, configure it specifically
    if 'DISPLAY_DUPLICATES' in settings.QUERYCOUNT:
        duplicate_settings = settings.QUERYCOUNT['DISPLAY_DUPLICATES']
        if duplicate_settings is not None:
            duplicate_settings = int(duplicate_settings)
        QC_SETTINGS['DISPLAY_DUPLICATES'] = duplicate_settings

    # Apply the rest of the setting overrides
    for key in ['THRESHOLDS',
                'IGNORE_REQUEST_PATTERNS',
                'IGNORE_SQL_PATTERNS',
                'IGNORE_PATTERNS',
                'RESPONSE_HEADER']:
        if key in settings.QUERYCOUNT:
            QC_SETTINGS[key] = settings.QUERYCOUNT[key]

# Perform initial load of settings
_process_settings()

# Subscribe to setting changes, via unit tests, etc
setting_changed.connect(_process_settings)

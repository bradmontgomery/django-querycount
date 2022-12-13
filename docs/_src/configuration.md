# Configuration

There are two possible settings for this app: The first defines threshold
values used to color output, while the second allows you customize requests
that will be ignored by the middleware. The default settings are:

```python
QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG':0,
        'MIN_QUERY_COUNT_TO_LOG':0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count',
    'NOCOLOR': False,
}
```

The `QUERYCOUNT['THRESHOLDS']` settings will determine how many queries are
interpreted as high or medium (and the color-coded output). In previous versions
of this app, this settings was called `QUERYCOUNT_THRESHOLDS` and that setting
is still supported.

The `QUERYCOUNT['IGNORE_REQUEST_PATTERNS']` setting allows you to define a list of
regexp patterns that get applied to each request's path. If there is a match,
the middleware will not be applied to that request. For example, the following
setting would bypass the querycount middleware for all requests to the admin:

```python
QUERYCOUNT = {
    'IGNORE_REQUEST_PATTERNS': [r'^/admin/']
}
```

The `QUERYCOUNT['IGNORE_SQL_PATTERNS']` setting allows you to define a list of
regexp patterns that ignored to statistic sql query count. For example, the following
setting would bypass the querycount middleware for django-silk sql query:

```python
QUERYCOUNT = {
    'IGNORE_SQL_PATTERNS': [r'silk_']
}
```

The `QUERYCOUNT['RESPONSE_HEADER']` setting allows you to define a custom response
header that contains the total number of queries executed. To disable this header,
the supply `None` as the value:

```python
QUERYCOUNT = {
    'RESPONSE_HEADER': None
}
```

_New in 0.4.0_. The `QUERYCOUNT['DISPLAY_DUPLICATES']` setting allows you
to control how the most common duplicate queries are displayed. If the setting
is `None` (the default), duplicate queries are not displayed. Otherwise, this
should be an integer. For example, the following setting would always print the
5 most duplicated queries:

```python
QUERYCOUNT = {
    'DISPLAY_DUPLICATES': 5,
}
```

_New in 1.0.0_: The `QUERYCOUNT['NOCOLOR']` settings allows you to disable colorized
output in ther terminal.

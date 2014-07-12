"""
Settings for a simple "test app" that we'll build just for running queries.
"""


DEFAULT_SETTINGS = dict(
    DEBUG=True,
    INSTALLED_APPS=(
        'test_app',
        ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
            },
        },
    )

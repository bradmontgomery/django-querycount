History
-------

0.4.1
+++++

- Fixed an issue where previous request's queries didn't get reset.
- Minor output formatting

0.4.0
+++++

- Included a count for duplicate sql queries. (`issue #7 <https://github.com/bradmontgomery/django-querycount/issues/7>`_)
- Included a new setting option, ``DISPLAY_DUPLICATES`` to control how many
  duplicate queries are printed in the shell.


0.3.0
+++++

- Added `IGNORE_SQL_PATTERNS`. `PR #6 <https://github.com/bradmontgomery/django-querycount/pull/6>`_. Thanks @GitFree
- Changed `IGNORE_PATTERNS` setting to `IGNORE_REQUEST_PATTERNS` (but still
  support the old setting)

0.2.0
+++++

- Added an `IGNORE_PATTERNS` setting and ability to ignore certain http requests.
- Slight project reorganization.

0.1.1
+++++

- Minor update to dynamically put version number in setup.py

0.1.0
+++++

- Added "elapsed" and "query count" log thresholds. `PR #4 <https://github.com/bradmontgomery/django-querycount/pull/4>`_. Thanks @alonisser

0.0.0
+++++

- Initial version. Huge thanks to @mrrrgn for making this look like a real project.

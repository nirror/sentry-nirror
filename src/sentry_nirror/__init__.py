"""
sentry_github
~~~~~~~~~~~~~

:copyright: (c) 2014 by the Nirror Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-nirror').version
except Exception, e:
    VERSION = 'unknown'

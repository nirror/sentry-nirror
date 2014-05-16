"""
sentry_nirror.plugin
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by the Nirror Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from sentry.plugins.bases.issue import IssuePlugin
from sentry.models import Event

import sentry_nirror
import urllib
import Cookie
import os
import re
import six

class NirrorPlugin(IssuePlugin):
    author = 'Nirror Team'
    author_url = 'https://github.com/nirror/sentry-nirror'
    version = sentry_nirror.VERSION
    description = "Integrate Nirror by listing links to visits."
    resource_links = [
        ('Bug Tracker', 'https://github.com/nirror/sentry-nirror/issues'),
        ('Source', 'https://github.com/nirror/sentry-nirror'),
    ]

    slug = 'nirror'
    title = _('Nirror')
    conf_title = title
    conf_key = 'nirror'
    auth_provider = 'nirror'

    def widget(self, request, group, **kwargs):
        events = Event.objects.filter(group=group).order_by('-datetime')[:100]
        visits = []
        for ev in events:
            http_data = ev.data.get('sentry.interfaces.Http')
            if http_data is None:
                continue
            visit_path = None
            if 'cookies' in http_data and http_data['cookies']:
                visit_path = self.decode_cookies(http_data['cookies'], '_ni_v')
            elif 'headers' in http_data and 'cookie' in http_data['headers']:
                visit_path = self.decode_cookies(http_data['headers']['cookie'], '_ni_v')
            if visit_path is None:
                continue
            m = re.search('#sites/\w+/r/(\w+)/v/(.+)', visit_path)
            if m is None:
                continue
            visit = {}
            visit['name'] = 'User(%s) Visit#%s' % (m.group(1), m.group(2))
            visit['url'] = "https://app.nirror.com/"+visit_path
            visits.append(visit)
        context = {
            'group': group,
            'visits': visits
        }
        return self.render('widget.html', context)

    def decode_cookies(self, cookie, key):
        if isinstance(cookie, six.string_types):
            c = Cookie.SimpleCookie(cookie.encode('ascii', 'ignore'))
            return urllib.unquote(c[key].value).decode('utf-8') if key in c else None
        elif type(cookie) is dict and key in cookie:
            return cookie[key]
        else:
            return None


    def is_configured(self, request, project, **kwargs):
        return bool(self.get_option('repo', project))

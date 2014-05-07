"""
sentry_nirror.plugin
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
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
            if http_data is not None and 'headers' in http_data and 'cookie' in http_data['headers']:
                cookie_str = http_data['headers']['cookie'].encode('ascii', 'ignore')
                c = Cookie.SimpleCookie(cookie_str)
                if '_ni_v' in c:
                    visit_path = urllib.unquote(c['_ni_v'].value).decode('utf-8')
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

    def is_configured(self, request, project, **kwargs):
        return bool(self.get_option('repo', project))

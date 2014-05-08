sentry-nirror
=============

An extension for Sentry which integrates with Nirror. Specifically, it lists associated nirror visits
for each group of events.


Install
-------

Install the package via ``pip``::

    pip install sentry-nirror

Restart sentry (if your are using suvervisor)::

    supervisorctl restart sentry-web

In sentry, navigate to your project settings page. On the left pannel go to ``Manage Integrations`` and enable ``Nirror by Nirror Team`` plugin.

The plugin adds a widget on the event group page which lists associated nirror visits.

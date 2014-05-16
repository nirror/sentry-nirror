#!/usr/bin/env python
"""
sentry-nirror
=============

An extension for Sentry which integrates with Nirror. Specifically, it lists associated nirror visits
for each group of events.

:copyright: (c) 2014 by the Nirror Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


tests_require = [
    'nose',
]

install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-nirror',
    version='0.1.2',
    author='Tugdual de Kerviler',
    author_email='dekervit@gmail.com',
    url='http://github.com/nirror/sentry-nirror',
    description='A Sentry extension which integrates with Nirror.',
    long_description=__doc__,
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'github = sentry_nirror',
        ],
       'sentry.plugins': [
            'github = sentry_nirror.plugin:NirrorPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)

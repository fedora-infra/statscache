""" Setup file for statscache """

import os
import os.path
from setuptools import setup


def get_description():
    with open('README.rst', 'r') as f:
        return ''.join(f.readlines()[2:])

requires = [
    'fedmsg',
    'moksha.hub>=1.4.6',
    'fedmsg_meta_fedora_infrastructure',
    'sqlalchemy',
    'futures',
]

tests_require = [
    'nose',
    'freezegun'
]

# Note to packagers: Install or link the following files using the specfile:
#   'apache/stastcache.conf' -> '/etc/httpd/conf.d/statscache.conf'
#   'apache/statscache.wsgi' -> '/usr/share/statscache/statscache.wsgi'
#   'statscache/static/' -> '/usr/share/statscache/static/'

setup(
    name='statscache',
    version='0.0.4',
    description='Daemon to build and keep fedmsg statistics',
    long_description=get_description(),
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url="https://github.com/fedora-infra/statscache/",
    download_url="https://pypi.python.org/pypi/statscache/",
    license='LGPLv2+',
    install_requires=requires,
    tests_require=tests_require,
    test_suite='nose.collector',
    packages=[
        'statscache',
        'statscache/plugins',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'moksha.consumer': [
            "statscache_consumer = statscache.consumer:StatsConsumer",
        ],
        'moksha.producer': [
            "statscache_producer = statscache.producer:StatsProducer",
        ],
    },
)

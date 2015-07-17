""" Setup file for statscache """

import os
import os.path
from setuptools import setup


def get_description():
    with open('README.rst', 'r') as f:
        return ''.join(f.readlines()[2:])

def expand_directory(path):
    return map(lambda name: os.path.join(path, name), os.listdir(path))

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

# TODO: let a flag or option determine whether to actually install these
install_data = [
    ('/etc/httpd/conf.d/', ['apache/statscache.conf']),
    ('/usr/share/statscache/', ['apache/statscache.wsgi']),
    ('/usr/share/statscache/static/style',
        expand_directory('statscache/static/style/')),
    ('/usr/share/statscache/static/script',
        expand_directory('statscache/static/script/')),
]

setup(
    name='statscache',
    version='0.0.1',
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
    packages=['statscache'],
    include_package_data=True,
    data_files=install_data,
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

""" Setup file for statscache """

import os
import os.path
from setuptools import setup


def get_description():
    with open('README.rst', 'r') as f:
        return ''.join(f.readlines()[2:])

def get_requirements(requirements_file='requirements.txt'):
    """
    Get the contents of a file listing the requirements.

    Args:
        requirements_file (str): path to a requirements file

    Returns:
        list: the list of requirements, or an empty list if
              `requirements_file` could not be opened or read
    """
    lines = open(requirements_file).readlines()
    dependencies = []
    for line in lines:
        maybe_dep = line.strip()
        if maybe_dep.startswith('#'):
            # Skip pure comment lines
            continue
        if maybe_dep.startswith('git+'):
            # VCS reference for dev purposes, expect a trailing comment
            # with the normal requirement
            __, __, maybe_dep = maybe_dep.rpartition('#')
        else:
            # Ignore any trailing comment
            maybe_dep, __, __ = maybe_dep.partition('#')
        # Remove any whitespace and assume non-empty results are dependencies
        maybe_dep = maybe_dep.strip()
        if maybe_dep:
            dependencies.append(maybe_dep)
    return dependencies

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
    install_requires=get_requirements(),
    tests_require=get_requirements('requirements_test.txt'),
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

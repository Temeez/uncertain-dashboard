import re
from setuptools import setup

def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']

DEPENDENCY_LINKS = [
    'git+https://github.com/kelleyk/python-systemd#egg=python-systemd'
]

REQUIRED = [
    'Flask>=0.10',
    'Flask-Migrate>=1.7',
    'Flask-RESTful>=0.3.5',
    'Flask-Script>=2.0',
    'Flask-SQLAlchemy>=2.0',
    'python-systemd',
]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet',
]

setup(
    name='Uncertain-Dashboard',
    version=get_version('uncertaind/__init__.py'),
    url='http://github.com/temeez/dapper-badass-dashboard/',
    license='MIT',
    author='Teemu Nieminen',
    author_email='teemun.dev@gmail.com',
    description=('Simple dashboard for checking systemd services and disks.'),
    long_description=__doc__,
    packages=['uncertaind'],
    zip_safe=False,
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    dependency_links=DEPENDENCY_LINKS,
    install_requires=REQUIRED,
    classifiers=CLASSIFIERS
)
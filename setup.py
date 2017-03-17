#!/usr/bin/env python

from setuptools import setup
import re

with open('mcan/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

setup(
    name='mcan',
    version=version,
    keywords=('mcan', 'meican', 'auto order'),
    description='meican tools',
    long_description='meican tools ....',
    author='demokn',
    author_email='demo.knyang@gmail.com',
    url='http://github.com/demokn/mcan',
    packages=['mcan'],
    package_data={'': []},
    package_dir={'mcan': 'mcan'},
    include_package_data=True,
    install_requires=['requests', 'docopt'],
    tests_require=[],
    extras_require={},
    license='Apache 2.0',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mcan = mcan.console:main',
        ],
    },
)

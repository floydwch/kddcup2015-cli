#!/usr/bin/env python
# -*- coding: utf-8 -*-

PROJECT = 'kddcup2015-cli'
VERSION = '0.1.0'

from setuptools import setup, find_packages

long_description = \
    'https://github.com/floydsoft/kddcup2015-cli/blob/master/README.md'

setup(
    name=PROJECT,
    version=VERSION,

    description='An unofficial command line tool for KDD Cup 2015.',
    long_description=long_description,

    author='floydsoft',
    author_email='floydsoft@gmail.com',

    url='https://github.com/floydsoft/kddcup2015-cli',
    download_url='https://github.com/floydsoft/kddcup2015-cli/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'RoboBrowser', 'pyquery',
        'requests[security]', 'python-dateutil'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'kdd = kddcup2015_cli.main:main'
        ],
        'kddcup2015_cli': [
            'submit = kddcup2015_cli.submit:Submit',
            'config = kddcup2015_cli.config:Config',
            'download = kddcup2015_cli.download:Download',
            'rank = kddcup2015_cli.rank:Rank',
            'score = kddcup2015_cli.score:Score'
        ],
    },

    zip_safe=False,
)

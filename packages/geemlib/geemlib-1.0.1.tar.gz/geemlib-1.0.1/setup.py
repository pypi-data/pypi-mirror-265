#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup config for installing the package."""

from setuptools import setup
# from geemlib.Changelog import GeemlibChangelog as cl


desc_short = 'This is the Geemlib.'
desc = open('README.md', 'r').read()

requirements = [
    'requests>=2.0',
    'beautifulsoup4>=4.0',
]

setup(
    name='geemlib',
    version='1.0.1',
    description=desc_short,
    long_description=desc,
    long_description_content_type='text/markdown',
    author="darkgeem",
    author_email="darkgeem@pyrokinesis.fr",
    url="https://git.pyrokinesis.fr/darkgeem/geemlib",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
    ],
    packages=[
        'geemlib',
        'geemlib.Changelog',
        'geemlib.Web',
    ],
    entry_points={
        'console_scripts': [
            'geemlib = geemlib.geemlib:main',
        ]
    },
    install_requires=requirements,
    license="WTFPL",
    license_files=["LICEN[CS]E*"],
    project_urls={
        'Source': 'https://git.pyrokinesis.fr/darkgeem/geemlib',
        'Support': 'https://discord.gg/KdRmyRrA48',
    },
)

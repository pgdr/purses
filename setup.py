#!/usr/bin/env python

from setuptools import setup

setup(
    name="purses",
    version="0.0.13",
    packages=[
        "purses",
    ],
    author="Pal.Drange@uib.no",
    author_email="Pal.Drange@uib.no",
    description="Purses, a Pandas Curses",
    tests_require=[
        "pandas",
    ],
    install_requires=["pandas", "npyscreen"],
    test_suite="tests",
    entry_points={"console_scripts": ["purses = purses:main"]},
)

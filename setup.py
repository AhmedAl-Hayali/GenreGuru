#!/usr/bin/env python
from setuptools import setup, find_packages

setup_info = dict(
    name = 'GenreGuru',
    packages = [pkg for pkg in find_packages(['src', 'test'])]
)

setup(**setup_info)
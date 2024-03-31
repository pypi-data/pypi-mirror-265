#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="dvaa",
    version="0.4.2",
    description="Lightweight data validation and adaptation library for Python",
    author="Rayan Haddad",
    author_email="rayan.m.haddad@proton.me",
    packages=find_packages(),
    install_requires=["decorator"],
    keywords="validation adaptation typechecking jsonschema",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
)

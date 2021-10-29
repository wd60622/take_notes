#!/usr/bin/env python

from setuptools import setup

setup(
    name="take_notes",
    version="0.1.0",
    author="William Dean",
    author_email="wdean@homepartners.com",
    description="Quickly take different notes.",
    packages=["take_notes"],
    scripts=["scripts/notes"],
    install_requires=["typer"],
)

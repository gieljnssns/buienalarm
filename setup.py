# python setup.py --dry-run --verbose install

from distutils.core import setup

import setuptools

setuptools.setup(
    name="pybuienalarm",
    version="0.0.11",  # Should be updated with new versions
    author="Giel Janssens",
    author_email="",
    py_modules=["pybuienalarm"],
    packages=["buienalarm"],
    package_dir={"buienalarm": "buienalarm"},
    scripts=[],
    data_files=[],
    url="https://github.com/gieljnssns/buienalarm",
    license="MIT",
    description="Simple API to access Buienalarm data. ",
    long_description=open("README.md").read(),
)

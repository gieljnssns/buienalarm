from setuptools import setup

setup(
    name="pybuienalarm",
    version="0.1.1",
    packages=["buienalarm"],
    package_data={
        "buienalarm": ["py.typed"],
    },
    url="https://github.com/gieljnssns/buienalarm",
    license="MIT",
    author="Giel Janssens",
    author_email="gieljnssns@vivaldi.net",
    description="Simple API to access Buienalarm data.",
    install_requires=["requests"],
    entry_points={"console_scripts": ["buienalarm=buienalarm.cli:main"]},
)

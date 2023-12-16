import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="Testing",
    version="0.0.1",
    author="Example Author",
    author_email="example@gmail.com",
    description="An example project",
    license="CodeVault License Agreement",
    keywords=["example", "project"],
    url="https://example.docs",

    # Path to the source: MainFolder/toolname/main.py
    # Path we're at: MainFolder/setup.py
    packages=find_packages(),

    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: Other/Proprietary License",
    ],
)

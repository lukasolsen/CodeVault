from setuptools import setup, find_packages

setup(
    name='cryptoguard',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['cryptoguard = cryptoguard.cryptoguard:main']
    },
    install_requires=[
        'termcolor',
        # Add other dependencies here
    ],
)

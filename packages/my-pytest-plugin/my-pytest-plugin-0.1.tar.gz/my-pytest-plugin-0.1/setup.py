# setup.py

from setuptools import setup, find_packages

setup(
    name='my-pytest-plugin',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'pytest11': [
            'my_pytest_plugin = my_pytest_plugin.my_pytest_plugin'
        ]
    },
    install_requires=['pytest'],
)

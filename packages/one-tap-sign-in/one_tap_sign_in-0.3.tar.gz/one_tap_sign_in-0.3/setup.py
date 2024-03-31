# setup.py

from setuptools import setup, find_packages

setup(
    name='one_tap_sign_in',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
)

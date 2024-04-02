# setup.py

from setuptools import setup, find_packages

setup(
    name='phone_email_auth',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
)

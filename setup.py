# setup.py

from setuptools import setup, find_packages

setup(
    name='commontools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pymysql',
    ],
)

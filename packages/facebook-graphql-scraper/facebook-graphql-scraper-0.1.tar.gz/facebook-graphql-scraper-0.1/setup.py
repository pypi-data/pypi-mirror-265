# -*- coding: utf-8 -*-
import setuptools
from setuptools import setup, find_packages

setup(
    name='facebook-graphql-scraper',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='Implement Facebook scraper for post data retrieval',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='FaustRen',
    author_email='faustren1z@gmail.com',
    url='https://github.com/FaustRen/facebook_graphql_scraper',
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)

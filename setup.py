#!/bin/env python3

from setuptools import setup, find_packages

with open("LICENSE.txt", 'r') as f:
    license_text = f.read()

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="fsxlcw",
    version="1.0.0",
    description='A python package that sends AWS FSxL quota metrics to AWS CloudWatch.',
    license=license_text,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matteo Mazzanti',
    author_email='mmmazzan@amazon.com',
    url="https://gitlab.aws.dev/fsxl-quota-metric-to-cw/fsxl-quota-metric-to-cw",
    entry_points={
        'console_scripts':[
            'fsxl-2cw = fsxlcw.main:main',
            'fsxl-diskfill = fsxlcw.utils.diskfill:main'
        ],
    },
    packages=find_packages(),
    package_dir={'fsxlcw': 'fsxlcw'},
    package_data={'fsxlcw': ['conf/*.yaml']},
    # automatically discover all packages and subpackages under package_dir
    python_requires=">=3.6.8",
    install_requires=[
        "boto3",
        "botocore >= 1.22.1",
        "pyyaml",
        "requests",
    ],
)

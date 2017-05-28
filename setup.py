"""CloudWatch logging handlers setup module.

Based on setuptools
"""

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='cloudwath_handlers',

    version='0.1.0',

    description='Python logging handlers for AWS CloudWatch service',
    long_description=long_description,

    url='https://github.com/mligus/cloudwatch-handlers',

    author='Max Ligus',
    author_email='max.ligus@gmail.com',

    license='MIT',

    # Description  at https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='logging handlers aws cloudwatch development',

    packages=find_packages(exclude=['docs', 'tests']),

    setup_requires=[
        'pytest-runner',
    ],

    install_requires=[
        'boto3>=1.4.4',
    ],

    tests_require=[
        'pytest>=3.1.0',
        'pytest-cov>=2.5.1',
     ],

)

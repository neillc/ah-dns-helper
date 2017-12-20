"""The setup tools configuration for this project. Based on the setuptools
sample project.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ah_dns_helper',
    version='0.0.1dev1',
    description='A simple helper script to get dns info about a domain.',
    long_description=long_description,
    url='https://github.com/neillc/ah-dns-helper',
    author='Neill Cox',
    author_email='neill.cox@ingenious.com.au',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Technical Staff',
        'Topic :: DNS :: Information',
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='dns information about a domain',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['dnspython3'],
    python_requires='>=3',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'ah_dns_helper=ah_dns_helper:main',
        ],
    },
)

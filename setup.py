#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'watchdog>=2.1.6', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Benoit Coste",
    author_email='benoit.coste@protonmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'code-assist=fix_tox.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='fix_tox',
    name='fix_tox',
    packages=find_packages(include=['fix_tox', 'fix_tox.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/wizmer/fix_tox',
    version='0.1.0',
    zip_safe=False,
)

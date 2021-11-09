"""Console script for fix_tox."""
import re
import sys
from pathlib import Path

import click

import fix_tox.fix_tox as fixer
from fix_tox.fix_setup import _check_existing_import


@click.group()
def cli():
    '''The main click group'''

@cli.command()
@click.argument('logfile')
def fix_tox(logfile):
    '''Fix setup.py'''
    fixer.fix(Path(logfile), Path('setup.py'))

@cli.command()
@click.argument('module')
def add_dependency(module):
    '''Fix setup.py'''
    test_deps = {
        'pip',
        'bump2version',
        'wheel',
        'watchdog',
        'flake8',
        'tox',
        'coverage',
        'Sphinx',
        'twine',
        'pytest',
        'pymock',
        'pytest',
        'pytest-mock',
    }
    if module in test_deps:
        filename = Path('requirements_dev.txt')
        version = _check_existing_import(module)
        assert version
        with open(filename, 'a') as f:
            f.write(f'{module}>={version}')
    else:
        filename = Path('setup.py')
        fixer.add_dependency(filename, module)

@cli.command()
@click.argument('filename')
def add_test_file(filename):
    import fix_tox.testing

    fix_tox.testing.add_test_file(filename)


@cli.command()
@click.argument('root_dir')
def watch(root_dir):
    import fix_tox.watcher
    fix_tox.watcher.watch(root_dir)

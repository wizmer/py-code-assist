"""Main module."""

import re

import click

from fix_tox.fix_setup import add_missing_module

MISSING_MODULE = 'ModuleNotFoundError: No module named \'(.*?)\''


def add_dependency(setup_file, dep):
    '''Add a missing dependency to a setup.py file.'''
    lines = add_missing_module(setup_file, dep)

    print("setup_file: {}".format(setup_file))
    with setup_file.open('w') as f:
        f.write(lines)

def get_missing_module(filename):
    lines = open(filename).readlines()
    for line in lines:
        m = re.search(MISSING_MODULE, line)
        if m:
            return m.groups()[0]


def fix(logfile, setup_file):
    missing = get_missing_module(logfile)
    if not missing:
        return
    non_matching_module_names = {
        'yaml': 'pyyaml',
    }
    missing = non_matching_module_names.get(missing, missing)

    if missing not in open(setup_file).read() and \
       click.confirm(f'Would you like to add module: {missing} to setup.py',
                                 default=True):
        add_dependency(setup_file, missing)

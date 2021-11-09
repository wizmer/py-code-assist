import imp
import importlib
import re
from distutils.core import run_setup

import pip
import pkg_resources


def _check_existing_import(module):
    '''Check if an import is already installed.

    Returns:
        The package version number.
    '''
    try:
        pkg = pkg_resources.get_distribution(module)
    except pkg_resources.DistributionNotFound:
        print('Installing missing package')
        pip.main(['install', module])
        pkg = pkg_resources.get_distribution(module)

    return pkg.version

def add_missing_module(setup_path, module_name):
    '''Returns the setup.py body with the missing dependency added.'''
    result = run_setup(str(setup_path), stop_after="init")

    first_dependency = result.install_requires[0]

    lines = open(setup_path).read()
    m = re.search(fr'({first_dependency})(.)', lines)
    quote = m.groups()[1]
    version = _check_existing_import(module_name)
    lines = lines.replace(m.group(), f'{m.group()}, {quote}{module_name}>={version}{quote}')

    return lines

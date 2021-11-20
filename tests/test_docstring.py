from pathlib import Path

import pytest


import code_assist.docstring as tested
from code_assist.testing import corresponding_module_name

DATA = Path(__file__).parent / 'data'


def test_generate_docstring():
    sample_file = DATA / '../../code_assist/fix_tox.py'
    assert sample_file.exists()
    result = tested.generate_docstring(sample_file, 'add_dependency')
    print('\n')
    print(result)

def test_get_existing_docstring():
    sample_file = DATA / '../../code_assist/fix_tox.py'
    assert sample_file.exists()
    result = tested.get_existing_docstring(sample_file, 'fix')

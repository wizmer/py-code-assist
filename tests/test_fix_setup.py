from pathlib import Path

import pytest

import fix_tox.fix_setup as tested

DATA = Path(__file__).parent / 'data'

def test_check_existing_import():
    version = tested._check_existing_import('pyyaml')
    assert version

def test_fix_setup():
    lines = tested.add_missing_module(DATA / 'setup.py.example', 'pyyaml')
    assert 'pyyaml' in lines

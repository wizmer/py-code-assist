import os
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

import pytest

import fix_tox.testing as tested


@pytest.fixture()
def mock_python_project():
    '''Create a temp python project'''
    with TemporaryDirectory() as folder:
        folder = Path(folder)
        os.mknod(folder / 'setup.py')
        src_file = folder / 'a/b/c/d.py'
        src_file.parent.mkdir(parents=True)
        with src_file.open('w') as f:
            f.write(dedent(
            '''
            def a_function(a):
                print(a)

            def another_function(a):
                print(a)

            '''))
        assert src_file.exists()
        yield src_file

def test_add_test_file(mock_python_project):
    test_file = tested.add_test_file(mock_python_project)
    assert test_file.exists()
    assert 'import a.b.c.d as tested' in test_file.open().read()


def test_add_test_function(mock_python_project):
    test_file = tested.add_test_function(mock_python_project, 'my_func')
    print(test_file.open().read())

def test_add_missing_test_functions(mock_python_project):
    # tested.add_missing_test_functions('/home/bcoste/workspace/code-assist/fix_tox/testing.py')
    pass

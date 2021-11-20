import os
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

import pytest

import code_assist.testing as tested


@pytest.fixture()
def mock_python_project():
    """Create a temp python project

    And temporary change the current directory to it
    """
    origin = Path().absolute()
    with TemporaryDirectory() as folder:
        folder = Path(folder)
        with open(folder / "setup.py", 'w') as f:
            f.write('')
        src_file = folder / "a/b/c/d.py"
        src_file.parent.mkdir(parents=True)
        os.chdir(folder)
        with src_file.open("w") as f:
            f.write(
                dedent(
                    """
            def a_function(a):
                print(a)

            def another_function_with_args(args1, args2):
                print(a)

            """
                )
            )
        assert src_file.exists()
        yield src_file
    os.chdir(origin)


def test_add_test_file(mock_python_project):
    test_file = tested.add_test_file(mock_python_project)
    assert test_file.exists()
    assert "import a.b.c.d as tested" in test_file.open().read()


def test_add_test_function(mock_python_project):
    test_file = tested.add_test_function(
        mock_python_project,
        "another_function_with_args",
    )
    assert (
        "def test_another_function_with_args():\n"
        "    tested.another_function_with_args(args1, args2)"
    ) in test_file.open().read()


def test_add_missing_test_functions(mock_python_project):
    # tested.add_missing_test_functions('/home/bcoste/workspace/code-assist/fix_tox/testing.py')
    pass

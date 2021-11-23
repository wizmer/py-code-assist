import os
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

import pytest

import code_assist.testing as tested

DATA = Path(__file__).parent / "data"


@pytest.fixture()
def mock_python_project():
    """Create a temp python project

    And temporary change the current directory to it
    """
    origin = Path().absolute()
    tempdir = TemporaryDirectory()
    folder = Path(tempdir.name, "test-code-assist")
    folder.mkdir(exist_ok=True)
    os.mknod(folder / "setup.py")
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

        class AClass:
            def a_method(self, arg1, arg2):
                print(arg1, arg2)

        """
            )
        )
    assert src_file.exists()
    yield src_file
    os.chdir(origin)


def test_corresponding_test_filename(mock_python_project):
    filename = tested.corresponding_test_filename(mock_python_project)
    assert filename.relative_to(os.getcwd()) == Path("tests/b/c/test_d.py")


def test_add_test_file(mock_python_project):
    test_file = tested.add_test_file(mock_python_project)
    assert test_file.exists()
    with open(test_file) as f:
        assert "import a.b.c.d as tested" in f.read()


def test_add_test_function(mock_python_project):
    test_file = tested.add_test_function(
        mock_python_project,
        "another_function_with_args",
    )
    assert (
        "def test_another_function_with_args():\n"
        "    tested.another_function_with_args(args1, args2)"
    ) in test_file.open().read()

    test_file = tested.add_test_function(
        mock_python_project,
        "a_method",
        "AClass",
    )

    assert (DATA / "add-test-function.py").open().read() == test_file.open().read()

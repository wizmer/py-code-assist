from pathlib import Path
from textwrap import dedent

import pytest

import code_assist.docstring as tested
from code_assist.testing import corresponding_module_name

DATA = Path(__file__).parent / "data"


def test_generate_docstring():
    sample_file = DATA / "../../code_assist/fix_tox.py"
    assert sample_file.exists()
    result = tested.generate_docstring(sample_file, "add_dependency")
    assert result == "TODO: fill the func header\n\nArgs:\n    root: \n    dep: "


def test_get_existing_docstring():
    sample_file = DATA / "google_docstring_style.py"
    assert sample_file.exists()
    docstring, (start, end) = tested.get_docstring(
        sample_file, "func_missing_arg_in_docstring"
    )

    assert (
        docstring
        == """    \"\"\"Here is a function with a full docstring.

    Args:
        arg1: a long description that span on
          multiple lines, actually this one is spanning on
          three lines !
        arg2:
        arg3:
        arg4: a short description

    Here are more notes about the docstring.
    \"\"\"
"""
    )

    assert sample_file.exists()
    docstring, (start, end) = tested.get_docstring(
        sample_file, "docstring_args_on_multiple_lines"
    )

    assert (
        docstring
        == """    \"\"\"Here is a function with a full docstring.

    Args:
        arg1: a long description that span on
          multiple lines, actually this one is spanning on
          three lines !
        arg2:
        arg3:
        arg4: a short description
        arg5_spanning_on_multiple_lines:
        args6_for_more_fun:
        args7_to_ensure_more_lines:

    Here are more notes about the docstring.
    \"\"\"
"""
    )


def test_get_docstring_line_numbers():
    sample_file = DATA / "google_docstring_style.py"
    assert tested.get_docstring_line_numbers(
        sample_file, "func_missing_arg_in_docstring"
    ) == (4, 15)

    assert tested.get_docstring_line_numbers(
        sample_file, "docstring_args_on_multiple_lines"
    ) == (27, 38)

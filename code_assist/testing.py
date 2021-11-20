import inspect
import os
import os.path
import re
import sys
from pathlib import Path
from textwrap import dedent

import pkg_resources
from jinja2 import Template


def _fill_template(template_filename, **kwargs):
    cluster_template = pkg_resources.resource_filename(
        "code_assist", f"data/{template_filename}"
    )

    with open(cluster_template) as file_:
        template = Template(file_.read())
    return template.render(**kwargs)


def up_dir(filename, start):
    """
    Find a parent path producing a match on one of its entries.
    Without match an empty string is returned.

    :param start: absolute path or None
    :return: directory with a match on one of its entries

    >>> up_dir(lambda x: False)
    ''

    """

    if any(x == filename for x in os.listdir(start)):
        return start
    parent = os.path.dirname(start)
    if start == parent:
        rootres = start.replace("\\", "/").strip("/").replace(":", "")
        if len(rootres) == 1 and sys.platform == "win32":
            rootres = ""
        return rootres
    return up_dir(filename, start=parent)


def corresponding_test_filename(filename):
    """Return the corresponding test filename."""
    filename = Path(filename).resolve()
    root = up_dir("setup.py", filename.parent)
    assert root
    root = Path(root)
    hierarchy = Path(*filename.relative_to(root).parent.parts[2:])
    test_file = root / "tests" / hierarchy / ("test_" + filename.name)
    return test_file


def corresponding_module_name(filename):
    """Return the corresponding test filename."""
    filename = Path(filename).resolve()
    root = up_dir("setup.py", filename.parent)
    assert root
    root = Path(root)
    hierarchy = filename.relative_to(root).with_suffix("")
    return str(hierarchy).replace(os.sep, ".")


def add_test_file(filename):
    """Add the corresponding test file if it does not exists.

    Returns: the path to the test file.
    """
    filename = Path(filename)
    assert filename.exists()
    test_file = corresponding_test_filename(filename)

    if test_file.exists():
        return test_file

    test_file.parent.mkdir(parents=True, exist_ok=True)
    module_name = corresponding_module_name(filename)
    content = _fill_template("test_file.py.jinja2", module=module_name)
    with open(test_file, "w") as f:
        f.write(content)
    return test_file


def add_test_function(filename, original_function_name):
    """Add a test function in order to test original function"""

    module_name = corresponding_module_name(filename)
    module = __import__(module_name, fromlist=[""])
    the_func = module.__dict__[original_function_name]
    args = ", ".join(inspect.getfullargspec(the_func).args)
    test_file = add_test_file(filename)
    with test_file.open("a") as f:
        f.write(
            dedent(
                f"""

        def test_{original_function_name}():
            tested.{original_function_name}({args})
        """
            )
        )

    return test_file


def is_mod_function(mod, func):
    """Return True if the function is defined within the module_name

    This is useful to distinguish between function defined in the module
    and function imported from another module.
    """
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return [
        func.__name__ for func in mod.__dict__.values() if is_mod_function(mod, func)
    ]


def list_functions1(mod):
    return [
        func.__name__
        for func in mod.__dict__.itervalues()
        if is_mod_function(mod, func)
    ]


def add_missing_test_functions(filename):
    module_name = corresponding_module_name(filename)
    module = __import__(module_name, fromlist=[""])

    test_name = corresponding_test_filename(filename)

    function_signature = r"def (\w+)\s*\((.*?)\):"
    test_functions = set()
    for line in test_name.open():
        m = re.search(function_signature, line)
        if m:
            test_functions.add(m.groups()[0])

    missing_tests = set(list_functions(module)) - test_functions
    for missing in missing_tests:
        add_test_function(filename, missing)

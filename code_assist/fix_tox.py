"""Main module."""

import re
from pathlib import Path

import click

from code_assist.fix_setup import add_missing_module, _check_existing_import


MISSING_MODULE = "ModuleNotFoundError: No module named '(.*?)'"


def add_dependency(root, dep):
    """Add a missing dependency to a setup.py or dependency file."""
    setup_file = Path(root, "setup.py")
    req_file = Path(root, "requirements.txt")
    req_dev_file = Path(root, "requirements_dev.txt")

    test_deps = {
        "pip",
        "bump2version",
        "wheel",
        "watchdog",
        "flake8",
        "tox",
        "coverage",
        "Sphinx",
        "twine",
        "pytest",
        "pymock",
        "pytest",
        "pytest-mock",
    }

    if dep in test_deps:
        if req_dev_file.exists():
            the_file = req_dev_file
        else:
            return
    else:
        the_file = req_file if req_file.exists() else setup_file

    if dep not in open(the_file).read():
        if not click.confirm(
            f"Would you like to add module: {dep} to {the_file}", default=True
        ):
            return

    if the_file in {req_dev_file, req_file}:
        version = _check_existing_import(dep)
        assert version
        with open(the_file, "a") as f:
            f.write(f"{dep}>={version}")
    else:
        filename = Path("setup.py")
        lines = add_missing_module(setup_file, dep)
        with setup_file.open("w") as f:
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
        "yaml": "pyyaml",
    }
    missing = non_matching_module_names.get(missing, missing)

    add_dependency(".", missing)

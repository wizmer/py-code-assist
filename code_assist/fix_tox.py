"""Main module."""

import re
from pathlib import Path

import click

from code_assist.fix_setup import _check_existing_import, add_missing_module

MISSING_MODULE = "ModuleNotFoundError: No module named '(.*?)'"
MISSING_PYTEST_COV = "unrecognized arguments: --cov-report"


def add_dependency(root, dep):
    """Add a missing dependency to a setup.py or dependency file."""
    setup_file = Path(root, "setup.py")
    req_file = Path(root, "requirements.txt")
    req_dev_file = Path(root, "requirements_dev.txt")

    test_deps = {
        "pip",
        "black",
        "bump2version",
        "wheel",
        "watchdog",
        "flake8",
        "isort",
        "tox",
        "coverage",
        "Sphinx",
        "twine",
        "pytest",
        "pymock",
        "pytest",
        "pytest-mock",
        "pytest-cov",
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
            f.write(f"{dep}>={version}\n")
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
        if MISSING_PYTEST_COV in line:
            return "pytest-cov"


def fix(logfile):
    """Attempt to fix everything it can from reading the log file

    Args:
        logfile: the tox stdout/stderr log file
    """
    missing = get_missing_module(logfile)
    if not missing:
        return
    non_matching_module_names = {
        "yaml": "pyyaml",
    }
    missing = non_matching_module_names.get(missing, missing)

    add_dependency(".", missing)

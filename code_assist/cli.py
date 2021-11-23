"""Console script for fix_tox."""
import re
import sys
from pathlib import Path

import click

import code_assist.fix_tox as fixer
from code_assist.fix_setup import _check_existing_import


@click.group()
def cli():
    """The main click group"""


@cli.command()
@click.argument("logfile")
def fix_tox(logfile):
    """Fix setup.py

    It will try to add the missing imports if it is detected that the were a MissingImportError
    """
    fixer.fix(Path(logfile))


@cli.command()
@click.argument("module")
def add_dependency(module):
    """Fix setup.py"""
    fixer.add_dependency(".", module)


@cli.command()
@click.argument("filename")
def add_test_file(filename):
    import code_assist.testing

    code_assist.testing.add_test_file(filename)


@cli.command()
@click.argument("filename")
@click.argument("function_name")
@click.option("--class-name", default=None)
def add_test_function(filename, function_name, class_name):
    import code_assist.testing

    code_assist.testing.add_test_function(filename, function_name, class_name)


@cli.command()
@click.argument("root_dir")
def watch(root_dir):
    import code_assist.watcher

    code_assist.watcher.watch(root_dir)

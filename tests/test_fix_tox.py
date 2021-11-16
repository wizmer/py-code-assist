from pathlib import Path

import pytest

import code_assist.fix_tox as tested

DATA = Path(__file__).parent / "data"


def test_add_dependency(mocker):
    mocker.patch("code_assist.fix_tox.click.confirm")
    tested.add_dependency(DATA / "package-with-req-file", "statsmodels")

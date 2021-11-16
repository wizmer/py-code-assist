import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

import code_assist.fix_tox as tested


DATA = Path(__file__).parent / "data"


def test_add_dependency(mocker):
    mocker.patch("code_assist.fix_tox.click.confirm")

    with TemporaryDirectory() as folder:
        folder = Path(folder)
        package = folder / "package"
        shutil.copytree(DATA / "package-with-req-file", package)

        req_file = package / "requirements.txt"

        assert req_file.exists()
        assert "statsmodels" not in req_file.open().read()
        tested.add_dependency(package, "statsmodels")
        assert "statsmodels" in req_file.open().read()

from pathlib import Path

from hml.types import PathLike


def test_path_like():
    assert isinstance(Path.cwd(), PathLike)
    assert isinstance(str(Path.cwd()), PathLike)

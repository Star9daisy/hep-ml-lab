import shutil
from pathlib import Path

import pytest

from hml.generators import Madgraph5, Madgraph5MultiRun, Madgraph5Run


def test_Madgraph5(tmp_path):
    with pytest.raises(EnvironmentError):
        Madgraph5(processes=["p p > t t~"], executable="wrong_executable")

    g = Madgraph5(
        executable="mg5_aMC",
        definitions={"p": "p b b~", "j": "j b b~"},
        model="sm",
        processes=[
            "p p > w+ z, w+ > j j, z > ve ve~",
            "p p > w- z, w- > j j, z > ve ve~",
        ],
        output=tmp_path / "demo",
    )

    with pytest.raises(ValueError):
        g.launch(shower="wrong_shower")  # type: ignore
    with pytest.raises(ValueError):
        g.launch(detector="wrong_detector")  # type: ignore

    g.launch(settings={"nevents": 100})
    g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"nevents": 100},
        cards=["./tests/scripts/delphes_card_eflow.dat"],
        multi_run=2,
    )
    g.summary()

    assert len(Madgraph5.from_output(tmp_path / "demo").runs) == 2
    with pytest.raises(FileNotFoundError):
        Madgraph5.from_output(tmp_path / "wrong_dir")
    with pytest.raises(FileNotFoundError):
        Madgraph5MultiRun.from_name("run_01", tmp_path / "wrong_dir")
    with pytest.raises(FileNotFoundError):
        Madgraph5Run.from_directory(tmp_path / "wrong_dir/Events/run_01_0")

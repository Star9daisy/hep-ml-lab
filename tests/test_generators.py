import shutil
from pathlib import Path

import cppyy
import pytest

from hml.generators import Madgraph5, MG5Run


def test_Madgraph5():
    data_dir = Path("./tests/data")
    shutil.rmtree(data_dir, ignore_errors=True)
    data_dir.mkdir()

    # executable x
    with pytest.raises(EnvironmentError):
        _ = Madgraph5(executable="wrong_executable", output="./tests/data")
    # executable ✔
    _ = Madgraph5(executable="mg5_aMC", output="./tests/data")

    # model path ✔
    _ = Madgraph5(executable="mg5_aMC", output="./tests/data", model="./tests/data")
    # model path x, model name ✔
    _ = Madgraph5(executable="mg5_aMC", output="./tests/data", model="sm")

    # card path ✔
    _ = Madgraph5(executable="mg5_aMC", output="./tests/data", cards=["./tests/data"])
    # card path x -> FileNotFoundError
    with pytest.raises(FileNotFoundError):
        _ = Madgraph5(
            executable="mg5_aMC", output="./tests/data", cards=["./tests/wrong_card"]
        )

    g = Madgraph5(
        executable="mg5_aMC",
        definitions={"p": "p b b~", "j": "j b b~"},
        processes=[
            "p p > w+ z, w+ > j j, z > ve ve~",
            "p p > w- z, w- > j j, z > ve ve~",
        ],
        output="./tests/data/demo",
        shower="Pythia8",
        detector="Delphes",
        cards=["./tests/scripts/delphes_card_eflow.dat"],
        n_events=100,
        seed=42,
    )

    assert isinstance(g.executable, Path)
    assert isinstance(g.output, Path)
    assert isinstance(g.model, (Path, str))
    assert isinstance(g.definitions, dict)
    assert isinstance(g.processes, list)

    # output x
    first_content = "\n".join(g.commands)
    assert "import model" in first_content
    assert "define" in first_content
    assert "generate" in first_content
    assert "output" in first_content
    assert "launch -i" in first_content
    assert "multi_run 1" in first_content
    assert "shower=Pythia8" in first_content
    assert "detector=Delphes" in first_content
    assert "set nevents 100" in first_content
    assert "set iseed 42" in first_content
    assert "print_results" in first_content

    g.n_events = 200
    g.n_events_per_subrun = 100
    assert "multi_run 2" in "\n".join(g.commands)

    g.n_events = 250
    g.n_events_per_subrun = 100
    assert "multi_run 3" in "\n".join(g.commands)

    g.n_events = 100

    g.launch()
    assert isinstance(g.runs, list)
    assert len(g.runs) == 1
    assert isinstance(g.runs[0], MG5Run)

    # output ✔
    # second_content = "\n".join(g.commands)
    # assert not "import model" in second_content
    # assert not "define" in second_content
    # assert not "generate" in second_content
    # assert not "output" in second_content
    g.launch()
    assert len(g.runs) == 2
    assert g.runs[0].cross_section == g.runs[1].cross_section

    g.remove("run_2")
    assert len(g.runs) == 1

    g.launch(new_output=True)
    assert len(g.runs) == 1

    with pytest.raises(FileNotFoundError):
        _ = MG5Run("wrong_dir")

    run_01 = MG5Run(g.output / "run_1")
    assert run_01.cross_section == g.runs[0].cross_section
    assert run_01.n_events == run_01.events.GetEntries()
    run_01.events.Reset()

    g.summary()
    g.clean()
    assert g.output.exists() is False

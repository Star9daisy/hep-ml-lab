import shutil
from pathlib import Path

import pytest

from hml.new_generators import Madgraph5, Madgraph5MultiRun, Madgraph5Run

data_dir = Path("./tests/data")
shutil.rmtree(data_dir, ignore_errors=True)
data_dir.mkdir()


def test_Madgraph5(tmpdir):
    demo_output = tmpdir / "test"
    wrong_output = tmpdir / "wrong"

    # Wrong executable ------------------------------------------------------- #
    with pytest.raises(EnvironmentError):
        Madgraph5(
            processes=["p p > w+ j, w+ > j j", "p p > w- j, w- > j j"],
            executable="wrong_executable",
            output=wrong_output,
        )

    # Wrong initialization --------------------------------------------------- #
    with pytest.raises(RuntimeError):
        Madgraph5(
            processes=["p p > w+ j, w+ > j j", "p p > w- j, w- > j j"],
            executable="mg5_aMC",
            model="wrong_model",
            output=wrong_output,
        )

    # ------------------------------------------------------------------------ #
    g = Madgraph5(
        processes=["p p > w+ j, w+ > j j", "p p > w- j, w- > j j"],
        executable="mg5_aMC",
        output=demo_output,
    )

    # Wrong shower and detector options -------------------------------------- #
    with pytest.raises(ValueError):
        g.launch(shower="wrong_shower")  # type: ignore
    with pytest.raises(ValueError):
        g.launch(detector="wrong_detector")  # type: ignore

    # ------------------------------------------------------------------------ #
    g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"iseed": 42, "nevents": 10},
        multi_run=2,
    )
    g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"iseed": 42, "nevents": 10},
    )

    assert len(g.runs) == 2
    g.summary()

    # Wrong output ----------------------------------------------------------- #
    with pytest.raises(FileNotFoundError):
        Madgraph5.from_output(wrong_output)

    # ------------------------------------------------------------------------ #
    existing_generator = Madgraph5.from_output(demo_output)
    assert len(existing_generator.runs) == len(g.runs)

    # ------------------------------------------------------------------------ #
    existing_mutlirun = Madgraph5MultiRun.from_name("run_01", demo_output)
    assert existing_mutlirun.n_events == g.runs[0].n_events

    existing_run = Madgraph5Run.from_directory(Path(demo_output / "Events/run_01_0"))
    assert existing_run.cross_section == g.runs[0].runs[0].cross_section

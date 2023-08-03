import shutil
from pathlib import Path

import cppyy
import pytest

from hml.generators import Madgraph5, MG5Run


def test_Madgraph5():
    data_dir = Path("./tests/data")
    shutil.rmtree(data_dir, ignore_errors=True)
    data_dir.mkdir()

    event_name1 = "pp2zj"
    expected_commands_run_01 = [
        "import model sm",
        "generate p p > z j, z > j j",
        f"output {Path.cwd()}/tests/data/{event_name1}",
        f"launch -i {Path.cwd()}/tests/data/{event_name1}",
        "multi_run 1",
        "shower=Pythia8",
        "detector=Delphes",
        "set nevents 10",
        "set iseed 42",
        f"{Path.cwd()}/tests/scripts/delphes_card_eflow.dat",
    ]
    expected_commands_run_02 = [
        f"launch -i {Path.cwd()}/tests/data/{event_name1}",
        "multi_run 1",
        "shower=Pythia8",
        "detector=Delphes",
        "set nevents 10",
        "set iseed 42",
        f"{Path.cwd()}/tests/scripts/delphes_card_eflow.dat",
    ]
    generator1 = Madgraph5(
        executable="mg5_aMC",
        processes=["p p > z j, z > j j"],
        output=f"./tests/data/{event_name1}",
        shower="Pythia8",
        detector="Delphes",
        cards=["./tests/scripts/delphes_card_eflow.dat"],
        settings={"nevents": 10, "iseed": 42},
    )
    assert generator1.commands == expected_commands_run_01
    generator1.launch()
    assert len(generator1.runs) == 1
    assert generator1.commands == expected_commands_run_02
    generator1.launch()
    assert len(generator1.runs) == 2
    assert generator1.runs[0].cross_section == generator1.runs[1].cross_section
    generator1.launch(new_output=True)
    assert len(generator1.runs) == 1

    event_name2 = "pp2wz"
    generator2 = Madgraph5(
        executable="mg5_aMC",
        definitions={"p": "p b b~", "j": "j b b~"},
        processes=[
            "p p > w+ z, w+ > j j, z > ve ve~",
            "p p > w- z, w- > j j, z > ve ve~",
        ],
        output=f"./tests/data/{event_name2}",
        shower="Pythia8",
        detector="Delphes",
        settings={"nevents": 90, "iseed": 42, "htjmin": 400},
        cards=["./tests/scripts/delphes_card_eflow.dat"],
        n_events_per_subrun=50,
    )
    generator2.launch()
    assert generator2.runs[0].n_events == 100
    generator2.settings["nevents"] = 50
    generator2.launch()
    assert generator2.runs[1].n_events == 50
    generator2.summary()

    # Remove the output directories and log files
    shutil.rmtree(Path.cwd() / f"tests/data/{event_name1}", ignore_errors=True)
    Path.unlink(Path.cwd() / f"tests/data/{event_name1}.log", missing_ok=True)
    shutil.rmtree(Path.cwd() / f"tests/data/{event_name2}", ignore_errors=True)
    Path.unlink(Path.cwd() / f"tests/data/{event_name2}.log", missing_ok=True)


def test_wrong_executable():
    event_name1 = "pp2zj"
    with pytest.raises(EnvironmentError):
        Madgraph5(
            executable="wrong_executable",
            processes="p p > z j, z > j j",
            output=f"./tests/data/{event_name1}",
            shower="Pythia8",
            detector="Delphes",
        )
    with pytest.raises(FileNotFoundError):
        Madgraph5(
            executable="mg5_aMC",
            processes="p p > z j, z > j j",
            output=f"./tests/data/{event_name1}",
            shower="Pythia8",
            detector="Delphes",
            cards=["./tests/scripts/wrong_card.dat"],
        )
    with pytest.raises(RuntimeError):
        generator1 = Madgraph5(
            executable="mg5_aMC",
            processes="[p p > z j, z > j j]",
            output=f"./tests/data/{event_name1}",
            shower="Pythia8",
            detector="Delphes",
        )
        generator1.launch()

    # Remove the output directories and log files
    shutil.rmtree(Path.cwd() / f"tests/data/{event_name1}", ignore_errors=True)
    Path.unlink(Path.cwd() / f"tests/data/{event_name1}.log", missing_ok=True)


if __name__ == "__main__":
    test_Madgraph5()

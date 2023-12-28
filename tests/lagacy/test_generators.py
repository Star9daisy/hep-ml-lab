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


def test_Madgraph5_seed_no_cards(tmp_path):
    # No seed ---------------------------------------------------------------- #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo1")
    g.launch(settings={"nevents": 100}, verbose=0)
    g.launch(settings={"nevents": 100}, verbose=0)

    # Check cross section
    assert g.runs[0].cross_section != g.runs[1].cross_section

    # With seed -------------------------------------------------------------- #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo2")
    g.launch(settings={"nevents": 100}, seed=42, verbose=0)
    g.launch(settings={"nevents": 100}, seed=42, verbose=0)

    # Check cross section
    assert g.runs[0].cross_section == g.runs[1].cross_section


def test_Madgraph5_seed_with_cards(tmp_path):
    # No seed, default cards ------------------------------------------------- #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo1")
    g.launch(shower="pythia8", detector="delphes", settings={"nevents": 100}, verbose=0)
    g.launch(shower="pythia8", detector="delphes", settings={"nevents": 100}, verbose=0)

    # Check cross section
    assert g.runs[0].cross_section != g.runs[1].cross_section

    # No seed, specific cards ------------------------------------------------ #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo2")
    g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"nevents": 100},
        cards=[
            "./tests/scripts/pythia8_card_42.dat",
            "./tests/scripts/delphes_card_42.dat",
        ],
        verbose=0,
    )
    g.launch(
        shower="pythia8",
        detector="delphes",
        settings={"nevents": 100},
        cards=[
            "./tests/scripts/pythia8_card_42.dat",
            "./tests/scripts/delphes_card_42.dat",
        ],
        verbose=0,
    )

    # Check cross section
    assert g.runs[0].cross_section != g.runs[1].cross_section

    # Check leaf size of every branch
    events0 = g.runs[0].events
    events1 = g.runs[1].events
    not_same = False
    for event0, event1 in zip(events0, events1):
        for b in events0.GetListOfBranches():
            obj0 = getattr(event0, b.GetName())
            obj1 = getattr(event1, b.GetName())
            if isinstance(obj0, int):
                not_same = True if obj0 != obj1 else False
            else:
                not_same = True if obj0.GetEntries() != obj1.GetEntries() else False
            if not_same:
                break
        if not_same:
            break
    assert not_same

    # Set seed, default cards ------------------------------------------------ #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo3")
    g.launch(
        shower="pythia8",
        detector="delphes",
        seed=42,
        settings={"nevents": 100},
        verbose=0,
    )
    g.launch(
        shower="pythia8",
        detector="delphes",
        seed=42,
        settings={"nevents": 100},
        verbose=0,
    )

    # Check cross section
    assert g.runs[0].cross_section == g.runs[1].cross_section

    # Check leaf size of every branch
    events0 = g.runs[0].events
    events1 = g.runs[1].events
    for event0, event1 in zip(events0, events1):
        for b in events0.GetListOfBranches():
            obj0 = getattr(event0, b.GetName())
            obj1 = getattr(event1, b.GetName())
            if isinstance(obj0, int):
                assert obj0 == obj1
            else:
                assert obj0.GetEntries() == obj1.GetEntries()

    # Set seed, specific cards ------------------------------------------------ #
    g = Madgraph5(processes=["p p > t t~"], output=tmp_path / "demo4")
    g.launch(
        shower="pythia8",
        detector="delphes",
        seed=123,
        settings={"nevents": 100},
        cards=[
            "./tests/scripts/pythia8_card_42.dat",
            "./tests/scripts/delphes_card_42.dat",
        ],
        verbose=0,
    )
    g.launch(
        shower="pythia8",
        detector="delphes",
        seed=123,
        settings={"nevents": 100},
        cards=[
            "./tests/scripts/pythia8_card_42.dat",
            "./tests/scripts/delphes_card_42.dat",
        ],
        verbose=0,
    )

    # Check cross section
    assert g.runs[0].cross_section == g.runs[1].cross_section

    # Check leaf size of every branch
    events0 = g.runs[0].events
    events1 = g.runs[1].events
    for event0, event1 in zip(events0, events1):
        for b in events0.GetListOfBranches():
            obj0 = getattr(event0, b.GetName())
            obj1 = getattr(event1, b.GetName())
            if isinstance(obj0, int):
                assert obj0 == obj1
            else:
                assert obj0.GetEntries() == obj1.GetEntries()

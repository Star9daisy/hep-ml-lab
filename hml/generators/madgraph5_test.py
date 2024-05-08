import shutil
from pathlib import Path

import pytest

from hml.generators import Madgraph5, Madgraph5Run


def test_madgraph5_default_init():
    g = Madgraph5()
    # Attributes ----------------------------------------------------------------- #
    with pytest.raises(ValueError):
        g.executable

    assert g.verbose == 1

    # Properties ----------------------------------------------------------------- #
    assert g.home is None
    assert g.version is None
    with pytest.raises(AttributeError):
        g.child
    with pytest.raises(AttributeError):
        g.processes
    with pytest.raises(AttributeError):
        g.runs

    # Methods -------------------------------------------------------------------- #
    with pytest.raises(AttributeError):
        g.import_model("sm")
    with pytest.raises(AttributeError):
        g.define(["j = j b b~"])
    with pytest.raises(AttributeError):
        g.generate(["p p > t t~"])
    with pytest.raises(AttributeError):
        g.output("test_pp2tt")
    with pytest.raises(AttributeError):
        g.launch()
    with pytest.raises(AttributeError):
        g.summary()


def test_madgraph5_init():
    g = Madgraph5(executable="mg5_aMC")

    assert g.executable == Path("/root/softwares/madgraph5/bin/mg5_aMC")
    assert g.home == Path("/root/softwares/madgraph5")
    assert g.version == "3.5.3"

    # Other cases
    with pytest.raises(FileNotFoundError):
        Madgraph5(executable="unknown")


def test_madgraph5_output():
    g = Madgraph5(executable="mg5_aMC")
    g.import_model("sm")
    g.define(["p = g u c d s u~ c~ d~ s~"])
    g.generate(["p p > t t~", "p p > t t~"])

    assert g.processes == ["p p > t t~", "p p > t t~"]

    g.display_diagrams("/tmp/Diagrams")
    shutil.rmtree("/tmp/Diagrams")

    # output is None
    g.output()
    assert g.output_dir.name == "PROC_sm_0"
    shutil.rmtree("PROC_sm_0")

    # output is specified
    g.output("/tmp/test_output")
    assert g.output_dir.name == "test_output"


def test_madgraph5_launch():
    g = Madgraph5(executable="mg5_aMC")
    g.generate(["p p > w+ z"])
    g.output("test_pp2wz")
    g.launch(settings={"nevents": 100})
    g.launch(settings={"nevents": 100}, multi_run=2)
    g.launch(
        shower="pythia8",
        detector="delphes",
        madspin="none",
        settings={"nevents": 100, "pt_min_pdg": {24: 250}, "pt_max_pdg": {24: 300}},
        seed=42,
        decays=["w+ > j j", "z > vl vl~"],
    )
    g.launch(
        shower="pythia8",
        detector="delphes",
        madspin="none",
        settings={"nevents": 100, "pt_min_pdg": {24: 250}, "pt_max_pdg": {24: 300}},
        seed=42,
        decays=["w+ > j j", "z > vl vl~"],
        cards=[
            "./tests/scripts/pythia8_card.dat",
            "./tests/scripts/delphes_card.dat",
        ],
    )

    assert isinstance(
        g.launch(
            shower="pythia8",
            detector="delphes",
            madspin="none",
            settings={"nevents": 100, "pt_min_pdg": {24: 250}, "pt_max_pdg": {24: 300}},
            seed=42,
            decays=["w+ > j j", "z > vl vl~"],
            cards=[
                "./tests/scripts/pythia8_card.dat",
                "./tests/scripts/delphes_card.dat",
            ],
            dry=True,
        ),
        list,
    )

    assert len(g.runs) == 4
    g.summary()

    loaded_g = Madgraph5.from_output("test_pp2wz", executable="mg5_aMC")
    assert len(loaded_g.runs) == 4
    assert loaded_g.processes == ["p p > w+ z"]

    shutil.rmtree("test_pp2wz")


def test_madgraph5_run_property():
    run = Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_01")

    assert run.directory == Path("./tests/data/pp2tt/Events/run_01")
    assert run.name == "run_01"
    assert run.collider == "pp:6500.0x6500.0"
    assert run.tag == "tag_1"
    assert run.seed == 42
    assert run.cross == 503.6
    assert run.error == 2.8
    assert run.n_events == 100
    assert len(run.sub_runs) == 0
    assert len(run.events()) == 1

    run = Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_02")

    assert run.directory == Path("./tests/data/pp2tt/Events/run_02")
    assert run.name == "run_02"
    assert run.collider == "pp:6500.0x6500.0"
    assert run.tag == "tag_1"
    assert run.seed == 48
    assert run.cross == 504.2
    assert run.error == 2
    assert run.n_events == 200
    assert len(run.sub_runs) == 2
    assert len(run.events()) == 2

    # Other cases
    with pytest.raises(FileNotFoundError):
        Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_03")

    with pytest.raises(ValueError):
        run = Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_01")
        run.events("lhe")


def test_madgraph5_run_special_methods():
    run = Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_01")

    assert (
        repr(run)
        == "Madgraph5Run run_01:\n- collider: pp:6500.0x6500.0\n- tag: tag_1\n- seed: 42\n- cross: 503.6\n- error: 2.8\n- n_events: 100"
    )

    run = Madgraph5Run(output_dir="./tests/data/pp2tt", name="run_02")

    assert (
        repr(run)
        == "Madgraph5Run run_02 (2 sub runs):\n- collider: pp:6500.0x6500.0\n- tag: tag_1\n- seed: 48\n- cross: 504.2\n- error: 2.0\n- n_events: 200"
    )

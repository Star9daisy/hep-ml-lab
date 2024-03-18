import shutil
from pathlib import Path

import pytest

from hml.generators import Madgraph5


def test_init():
    g = Madgraph5(executable="mg5_aMC")

    assert g.executable == Path("/root/softwares/madgraph5/bin/mg5_aMC")
    assert g.home == Path("/root/softwares/madgraph5")
    assert g.version == "3.5.3"
    assert repr(g) == "Madgraph5 v3.5.3"

    # Other cases
    with pytest.raises(FileNotFoundError):
        Madgraph5(executable="unknown")


def test_output():
    g = Madgraph5(executable="mg5_aMC")
    g.import_model("sm")
    g.define("p = g u c d s u~ c~ d~ s~")
    g.generate("p p > t t~", "p p > t t~")

    assert g.processes == ["p p > t t~", "p p > t t~"]

    g.display_diagrams("/tmp/Diagrams")
    with pytest.raises(FileExistsError):
        g.display_diagrams("/tmp/Diagrams")
    shutil.rmtree("/tmp/Diagrams")

    # output is None
    g.output()
    assert g.output_dir.name == "PROC_sm_0"
    shutil.rmtree("PROC_sm_0")

    # output is specified
    g.output("/tmp/test_output")
    assert g.output_dir.name == "test_output"

    # If not overwrite
    with pytest.raises(FileExistsError):
        g.output("/tmp/test_output", overwrite=False)


def test_launch():
    g = Madgraph5(executable="mg5_aMC")
    g.generate("p p > w+ z")
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
        str,
    )

    assert len(g.runs) == 4
    g.summary()

    loaded_g = Madgraph5.from_output("test_pp2wz", executable="mg5_aMC")
    assert len(loaded_g.runs) == 4
    assert loaded_g.processes == ["p p > w+ z"]

    shutil.rmtree("test_pp2wz")

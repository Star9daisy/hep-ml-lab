import pytest

from hml.generators import Madgraph5, Madgraph5Run


def test_madgraph5_run_for_single():
    g = Madgraph5Run("tests/data/pp2tt", "run_01")
    assert g.directory.as_posix() == "tests/data/pp2tt/Events/run_01"
    assert g.name == "run_01"
    assert g.collider == "pp:6500.0x6500.0"
    assert g.tag == "tag_1"
    assert g.seed == 42
    assert g.cross == 503.6
    assert g.error == 2.8
    assert g.n_events == 100
    assert len(g.sub_runs) == 0
    assert g.events().GetEntries() == 100


def test_madgraph5_run_for_multiple():
    g = Madgraph5Run("tests/data/pp2tt", "run_02")
    assert g.directory.as_posix() == "tests/data/pp2tt/Events/run_02"
    assert g.name == "run_02"
    assert g.collider == "pp:6500.0x6500.0"
    assert g.tag == "tag_1"
    assert g.seed == 48
    assert g.cross == 504.2
    assert g.error == 2.0
    assert g.n_events == 200
    assert len(g.sub_runs) == 2
    assert g.events().GetEntries() == 200


def test_madgraph5(tmp_path):
    g = Madgraph5("mg5_aMC")
    g.import_model("sm")
    g.define("p = g u c d s u~ c~ d~ s~")
    g.generate("p p > t t~")
    g.output(f"{tmp_path}/gen_pp2tt")
    g.launch(settings={"nevents": 100})
    g.launch(settings={"nevents": 100}, multi_run=2)
    assert len(g.runs) == 2
    assert g.processes == ["p p > t t~"]
    assert str(g) == "Madgraph5 v3.5.2"
    g.summary()

    g2 = Madgraph5.from_output(f"{tmp_path}/gen_pp2tt", "mg5_aMC")
    assert len(g2.runs) == 2

    # Wrong cases
    # Wrong executable
    with pytest.raises(FileNotFoundError):
        Madgraph5("wrong_executable")

    # Call .processes before generator.generate or Madgraph5.from_output
    with pytest.raises(AttributeError):
        _g = Madgraph5("mg5_aMC")
        print(_g.processes)

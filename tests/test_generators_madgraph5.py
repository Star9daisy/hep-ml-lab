from hml.generators import Madgraph5Run


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
    assert g.seed == 42
    assert g.cross == 503.7
    assert g.error == 2.0
    assert g.n_events == 200
    assert len(g.sub_runs) == 2
    assert g.events().GetEntries() == 200

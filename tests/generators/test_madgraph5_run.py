from pathlib import Path

import pytest

from hml.generators import Madgraph5Run


def test_property():
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


def test_special_methods():
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

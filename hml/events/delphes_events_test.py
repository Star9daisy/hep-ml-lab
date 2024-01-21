import pytest

from hml.events import DelphesEvents
from hml.types import Path


def test_delphes_events():
    tests_dir = "tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root"
    events = DelphesEvents(tests_dir)
    assert events.filepath == Path(tests_dir)
    assert len(events) == 100
    assert events[0]

    for event in events:
        assert event


def test_bad_filepath():
    with pytest.raises(ValueError):
        DelphesEvents("events.not_root")

    with pytest.raises(FileNotFoundError):
        DelphesEvents("events.root")

import pytest

from ..events.delphes_events import DelphesEvents
from .collective import Collective


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obj = Collective("Jet", 1, 3)
    assert obj.name == "Jet"
    assert obj.start == 1
    assert obj.stop == 3
    assert obj.objects == []
    assert obj.identifier == "Jet1:3"
    assert repr(obj) == "Jet1:3"
    assert obj.config == {
        "classname": "Collective",
        "name": "Jet",
        "start": 1,
        "stop": 3,
    }

    assert Collective("Jet").identifier == "Jet:"
    assert Collective("Jet", 1).identifier == "Jet1:"
    assert Collective("Jet", stop=3).identifier == "Jet:3"
    assert Collective("Jet", 1, 3).identifier == "Jet1:3"


def test_from_identifier():
    assert Collective.from_identifier("Jet1:3") == Collective("Jet", 1, 3)
    assert Collective.from_identifier("Jet1:3") != Collective("Jet", 1, 4)

    with pytest.raises(ValueError):
        Collective.from_identifier("Jet1")

    with pytest.raises(ValueError):
        Collective.from_identifier("Jet1.Constituents1")

    with pytest.raises(ValueError):
        Collective.from_identifier("Jet0, Jet1")


def test_from_config():
    obj = Collective("Jet", 1, 3)
    assert obj == Collective.from_config(obj.config)

    with pytest.raises(ValueError):
        Collective.from_config({"classname": "Unknown"})


def test_read(event):
    obj = Collective("Jet", 1).read(event)
    assert len(obj.objects) >= 1
    assert all(obj.objects) is True

    obj = Collective("Jet", 1, 3).read(event)
    assert len(obj.objects) == 2
    assert all(obj.objects) is True

    obj = Collective("Jet", 3, 6).read(event)
    assert len(obj.objects) == 3
    assert any(obj.objects) is True

    obj = Collective("Jet", 100, 101).read(event)
    assert len(obj.objects) == 1
    assert all(obj.objects) is False

    with pytest.raises(ValueError):
        Collective("Unknown", 0, 1).read(event)

    obj = Collective("Particles", 1, 3).read(event.Jet[0])
    assert len(obj.objects) == 2
    assert all(obj.objects) is True

    obj = Collective("Particles", 10, 110).read(event.Jet[0])
    assert len(obj.objects) == 100
    assert any(obj.objects) is True

    obj = Collective("Particles", 100, 101).read(event.Jet[0])
    assert len(obj.objects) == 1
    assert all(obj.objects) is False

    with pytest.raises(ValueError):
        Collective("Unknown", 0, 1).read(event.Jet[0])

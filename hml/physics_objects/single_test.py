import pytest

from ..events.delphes_events import DelphesEvents
from ..physics_objects.single import Single

# from ..physics_objects.single import SinglePhysicsObject
# from ..physics_objects.single import is_single_physics_object


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_attributes():
    obj = Single("Jet", 0)
    assert obj.name == "Jet"
    assert obj.index == 0
    assert obj.objects == []
    assert obj.identifier == "Jet0"
    assert repr(obj) == "Jet0"
    assert obj.config == {
        "classname": "Single",
        "name": "Jet",
        "index": 0,
    }


def test_from_identifier():
    assert Single.from_identifier("Jet0") == Single("Jet", 0)
    assert Single.from_identifier("Jet1") != Single("Jet", 0)

    with pytest.raises(ValueError):
        Single.from_identifier("Jet0,Jet1")

    with pytest.raises(ValueError):
        Single.from_identifier("Jet0.Constituents0")

    with pytest.raises(ValueError):
        Single.from_identifier("Jet1:3")


def test_from_config():
    obj = Single("Jet", 0)
    assert obj == Single.from_config(obj.config)

    with pytest.raises(ValueError):
        Single.from_config({"classname": "Unknown"})


def test_read(event):
    obj = Single("Jet", 0).read(event)
    assert len(obj.objects) == 1
    assert obj.objects[0] is not None

    obj = Single("Jet", 100).read(event)
    assert len(obj.objects) == 1
    assert obj.objects[0] is None

    with pytest.raises(ValueError):
        Single("Unknown", 0).read(event)

    obj = Single("Particles", 0).read(event.Jet[0])
    assert len(obj.objects) == 1
    assert obj.objects[0] is not None

    obj = Single("Particles", 100).read(event.Jet[0])
    assert len(obj.objects) == 1
    assert obj.objects[0] is None

    with pytest.raises(ValueError):
        Single("Unknown", 0).read(event.Jet[0])

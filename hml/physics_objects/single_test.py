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
    assert obj.field == "Jet"
    assert obj.index == 0
    assert obj.objects == []
    assert obj.id == "Jet0"
    assert repr(obj) == "Single: Jet0"
    assert obj.config == {
        "classname": "Single",
        "field": "Jet",
        "index": 0,
    }


def test_from_identifier():
    assert Single.from_id("Jet0") == Single("Jet", 0)
    assert Single.from_id("Jet1") != Single("Jet", 0)

    with pytest.raises(ValueError):
        Single.from_id("Jet0,Jet1")

    with pytest.raises(ValueError):
        Single.from_id("Jet0.Constituents0")

    with pytest.raises(ValueError):
        Single.from_id("Jet1:3")


def test_from_config():
    obj = Single("Jet", 0)
    assert obj == Single.from_config(obj.config)

    with pytest.raises(ValueError):
        Single.from_config({"classname": "Unknown"})


def test_read(event):
    assert len(Single("Jet", 0).read_ttree(event).objects) == 1
    assert len(Single("Jet", 100).read_ttree(event).objects) == 0

    with pytest.raises(ValueError):
        Single("Unknown", 0).read_ttree(event)

    assert len(Single("Constituents", 0).read_ttree(event.Jet[0]).objects) == 1
    assert len(Single("Constituents", 100).read_ttree(event.Jet[0]).objects) == 0

    with pytest.raises(ValueError):
        Single("Unknown", 0).read_ttree(event.Jet[0])

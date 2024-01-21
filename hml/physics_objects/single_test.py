import pytest

from ..events.delphes_events import DelphesEvents
from ..physics_objects.single import SinglePhysicsObject
from ..physics_objects.single import is_single_physics_object


@pytest.fixture
def event():
    events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
    yield events[0]


def test_validation_function():
    assert is_single_physics_object("") is False
    assert is_single_physics_object(None) is False

    assert is_single_physics_object("Jet0") is True
    assert is_single_physics_object(SinglePhysicsObject.from_name("Jet0")) is True

    assert is_single_physics_object("Jet0:") is False
    assert is_single_physics_object("Jet0.Constituents1") is False


def test_pattern():
    obj1 = SinglePhysicsObject("Jet", 0)
    obj2 = SinglePhysicsObject.from_name("Jet0")
    obj3 = SinglePhysicsObject.from_config(
        {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.index == 0
        assert obj.name == "Jet0"
        assert obj.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }


def test_bad_name():
    with pytest.raises(ValueError):
        SinglePhysicsObject.from_name("Jet")


def test_bad_config():
    with pytest.raises(ValueError):
        SinglePhysicsObject.from_config(
            {
                "class_name": None,
                "type": "Jet",
                "index": 0,
            }
        )


def test_read(event):
    obj = SinglePhysicsObject.from_name("Jet0")
    assert obj.read(event)


def test_read_bad_cases(event):
    obj = SinglePhysicsObject.from_name("BadSingle0")
    with pytest.raises(ValueError):
        obj.read(event)

    obj = SinglePhysicsObject.from_name("FatJet100")
    assert obj.read(event) is None

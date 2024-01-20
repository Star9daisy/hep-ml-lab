import pytest

from hml.events import DelphesEvents
from hml.physics_objects import CollectivePhysicsObject
from hml.physics_objects import is_collective_physics_object

events = DelphesEvents("tests/data/pp2tt/Events/run_01/tag_1_delphes_events.root")
event = events[0]


def test_validation_function():
    assert is_collective_physics_object("") is False
    assert is_collective_physics_object(None) is False

    assert is_collective_physics_object("Jet") is True
    assert is_collective_physics_object("Jet0:") is True
    assert is_collective_physics_object("Jet:1") is True
    assert is_collective_physics_object("Jet0:1") is True

    assert is_collective_physics_object("Jet:") is False
    assert is_collective_physics_object("Jet0") is False
    assert is_collective_physics_object("Jet0.Constituents1") is False


def test_pattern1():
    obj1 = CollectivePhysicsObject("Jet")
    obj2 = CollectivePhysicsObject.from_name("Jet")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": None,
            "end": None,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start is None
        assert obj.end is None
        assert obj.name == "Jet"
        assert obj.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": None,
            "end": None,
        }


def test_pattern2():
    obj1 = CollectivePhysicsObject("Jet", 0)
    obj2 = CollectivePhysicsObject.from_name("Jet0:")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": None,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start == 0
        assert obj.end is None
        assert obj.name == "Jet0:"
        assert obj.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": None,
        }


def test_pattern3():
    obj1 = CollectivePhysicsObject("Jet", None, 1)
    obj2 = CollectivePhysicsObject.from_name("Jet:1")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": None,
            "end": 1,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start is None
        assert obj.end == 1
        assert obj.name == "Jet:1"
        assert obj.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": None,
            "end": 1,
        }


def test_pattern4():
    obj1 = CollectivePhysicsObject("Jet", 0, 1)
    obj2 = CollectivePhysicsObject.from_name("Jet0:1")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": 1,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start == 0
        assert obj.end == 1
        assert obj.name == "Jet0:1"
        assert obj.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": 1,
        }


def test_bad_name():
    with pytest.raises(ValueError):
        CollectivePhysicsObject.from_name("Jet0")


def test_bad_config():
    with pytest.raises(ValueError):
        CollectivePhysicsObject.from_config(
            {
                "class_name": None,
                "type": "Jet",
                "start": 0,
                "end": 1,
            }
        )


def test_read():
    obj1 = CollectivePhysicsObject.from_name("Jet")
    assert len(obj1.read(event)) > 0

    obj2 = CollectivePhysicsObject.from_name("Jet0:")
    assert len(obj2.read(event)) > 0
    assert len(obj1.read(event)) == len(obj2.read(event))

    obj3 = CollectivePhysicsObject.from_name("Jet:1")
    assert len(obj3.read(event)) == 1

    obj3_with_none = CollectivePhysicsObject.from_name("Jet:100")
    assert len(obj3_with_none.read(event)) == 100

    obj4 = CollectivePhysicsObject.from_name("Jet0:1")
    assert len(obj4.read(event)) == 1
    assert len(obj3.read(event)) == len(obj4.read(event))

    obj4_with_none = CollectivePhysicsObject.from_name("Jet0:100")
    assert len(obj4_with_none.read(event)) == 100
    assert len(obj3_with_none.read(event)) == len(obj4_with_none.read(event))


def test_read_bad_cases():
    obj = CollectivePhysicsObject.from_name("BadCollective")
    with pytest.raises(ValueError):
        obj.read(event)

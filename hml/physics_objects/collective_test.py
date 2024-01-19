import pytest

from hml.physics_objects import CollectivePhysicsObject


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

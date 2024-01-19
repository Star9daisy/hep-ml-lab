import pytest

from hml.physics_objects import CollectivePhysicsObject


def test_pattern1():
    obj1 = CollectivePhysicsObject("Jet")
    obj2 = CollectivePhysicsObject.from_name("Jet")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": None,
            "collective_physics_object_end": None,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start is None
        assert obj.end is None
        assert obj.name == "Jet"
        assert obj.config == {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": None,
            "collective_physics_object_end": None,
        }


def test_pattern2():
    obj1 = CollectivePhysicsObject("Jet", 0)
    obj2 = CollectivePhysicsObject.from_name("Jet0:")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": 0,
            "collective_physics_object_end": None,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start == 0
        assert obj.end is None
        assert obj.name == "Jet0:"
        assert obj.config == {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": 0,
            "collective_physics_object_end": None,
        }


def test_pattern3():
    obj1 = CollectivePhysicsObject("Jet", None, 1)
    obj2 = CollectivePhysicsObject.from_name("Jet:1")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": None,
            "collective_physics_object_end": 1,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start is None
        assert obj.end == 1
        assert obj.name == "Jet:1"
        assert obj.config == {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": None,
            "collective_physics_object_end": 1,
        }


def test_pattern4():
    obj1 = CollectivePhysicsObject("Jet", 0, 1)
    obj2 = CollectivePhysicsObject.from_name("Jet0:1")
    obj3 = CollectivePhysicsObject.from_config(
        {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": 0,
            "collective_physics_object_end": 1,
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.type == "Jet"
        assert obj.start == 0
        assert obj.end == 1
        assert obj.name == "Jet0:1"
        assert obj.config == {
            "collective_physics_object_type": "Jet",
            "collective_physics_object_start": 0,
            "collective_physics_object_end": 1,
        }


def test_wrong_pattern():
    with pytest.raises(ValueError):
        CollectivePhysicsObject.from_name("Jet0")

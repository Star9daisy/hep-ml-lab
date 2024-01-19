import pytest

from hml.physics_objects import SinglePhysicsObject
from hml.physics_objects import is_single_physics_object


def test_validation_function():
    assert is_single_physics_object("Jet0") is True
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

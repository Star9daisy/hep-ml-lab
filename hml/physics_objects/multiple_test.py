import pytest

from hml.physics_objects import CollectivePhysicsObject
from hml.physics_objects import MultiplePhysicsObject
from hml.physics_objects import NestedPhysicsObject
from hml.physics_objects import SinglePhysicsObject
from hml.physics_objects import is_multiple_physics_object


def test_validation_function():
    assert is_multiple_physics_object("Jet0,Jet0") is True
    assert is_multiple_physics_object("Jet0,Jet0,Jet0") is True
    assert is_multiple_physics_object("Jet0,Jet0:1,Jet0.Constituents") is True

    assert is_multiple_physics_object("Jet0,") is False
    assert is_multiple_physics_object("Jet0") is False
    assert is_multiple_physics_object("Jet0:") is False


def test_pattern():
    obj1 = MultiplePhysicsObject(
        SinglePhysicsObject("Jet", 0),
        NestedPhysicsObject(
            SinglePhysicsObject("Jet", 0),
            SinglePhysicsObject("Constituents", 0),
        ),
        CollectivePhysicsObject("Jet", 1, 2),
    )
    obj2 = MultiplePhysicsObject.from_name("Jet0,Jet0.Constituents0,Jet1:2")
    obj3 = MultiplePhysicsObject.from_config(
        {
            "class_name": "MultiplePhysicsObject",
            "all_configs": [
                {
                    "class_name": "SinglePhysicsObject",
                    "type": "Jet",
                    "index": 0,
                },
                {
                    "class_name": "NestedPhysicsObject",
                    "main_config": {
                        "class_name": "SinglePhysicsObject",
                        "type": "Jet",
                        "index": 0,
                    },
                    "sub_config": {
                        "class_name": "SinglePhysicsObject",
                        "type": "Constituents",
                        "index": 0,
                    },
                },
                {
                    "class_name": "CollectivePhysicsObject",
                    "type": "Jet",
                    "start": 1,
                    "end": 2,
                },
            ],
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.all[0].type == "Jet"
        assert obj.all[0].index == 0
        assert obj.all[0].name == "Jet0"
        assert obj.all[0].config == {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }

        assert obj.all[1].main.type == "Jet"
        assert obj.all[1].main.index == 0
        assert obj.all[1].main.name == "Jet0"
        assert obj.all[1].main.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }
        assert obj.all[1].sub.type == "Constituents"
        assert obj.all[1].sub.index == 0
        assert obj.all[1].sub.name == "Constituents0"
        assert obj.all[1].sub.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Constituents",
            "index": 0,
        }

        assert obj.all[2].type == "Jet"
        assert obj.all[2].start == 1
        assert obj.all[2].end == 2
        assert obj.all[2].name == "Jet1:2"
        assert obj.all[2].config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 1,
            "end": 2,
        }

        assert obj.name == "Jet0,Jet0.Constituents0,Jet1:2"
        assert obj.config == {
            "class_name": "MultiplePhysicsObject",
            "all_configs": [
                {
                    "class_name": "SinglePhysicsObject",
                    "type": "Jet",
                    "index": 0,
                },
                {
                    "class_name": "NestedPhysicsObject",
                    "main_config": {
                        "class_name": "SinglePhysicsObject",
                        "type": "Jet",
                        "index": 0,
                    },
                    "sub_config": {
                        "class_name": "SinglePhysicsObject",
                        "type": "Constituents",
                        "index": 0,
                    },
                },
                {
                    "class_name": "CollectivePhysicsObject",
                    "type": "Jet",
                    "start": 1,
                    "end": 2,
                },
            ],
        }


def test_bad_name():
    with pytest.raises(ValueError):
        MultiplePhysicsObject.from_name("Jet0")


def test_bad_config():
    with pytest.raises(ValueError):
        MultiplePhysicsObject.from_config(
            {
                "class_name": None,
                "all_configs": [
                    {
                        "class_name": "SinglePhysicsObject",
                        "type": "Jet",
                        "index": 0,
                    },
                    {
                        "class_name": "NestedPhysicsObject",
                        "main_config": {
                            "class_name": "SinglePhysicsObject",
                            "type": "Jet",
                            "index": 0,
                        },
                        "sub_config": {
                            "class_name": "SinglePhysicsObject",
                            "type": "Constituents",
                            "index": 0,
                        },
                    },
                    {
                        "class_name": "CollectivePhysicsObject",
                        "type": "Jet",
                        "start": 1,
                        "end": 2,
                    },
                ],
            }
        )
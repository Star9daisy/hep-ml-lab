import pytest

from hml.physics_objects import CollectivePhysicsObject
from hml.physics_objects import NestedPhysicsObject
from hml.physics_objects import SinglePhysicsObject


def test_pattern_single_single():
    obj1 = NestedPhysicsObject(
        SinglePhysicsObject("Jet", 0),
        SinglePhysicsObject("Constituents", 1),
    )
    obj2 = NestedPhysicsObject.from_name("Jet0.Constituents1")
    obj3 = NestedPhysicsObject.from_config(
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
                "index": 1,
            },
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.main.type == "Jet"
        assert obj.main.index == 0
        assert obj.main.name == "Jet0"
        assert obj.main.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }

        assert obj.sub.type == "Constituents"
        assert obj.sub.index == 1
        assert obj.sub.name == "Constituents1"
        assert obj.sub.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Constituents",
            "index": 1,
        }

        assert obj.name == "Jet0.Constituents1"
        assert obj.config == {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Jet",
                "index": 0,
            },
            "sub_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Constituents",
                "index": 1,
            },
        }


def test_pattern_single_collective():
    obj1 = NestedPhysicsObject(
        SinglePhysicsObject("Jet", 0),
        CollectivePhysicsObject("Constituents", 1),
    )
    obj2 = NestedPhysicsObject.from_name("Jet0.Constituents1:")
    obj3 = NestedPhysicsObject.from_config(
        {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Jet",
                "index": 0,
            },
            "sub_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Constituents",
                "start": 1,
                "end": None,
            },
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.main.type == "Jet"
        assert obj.main.index == 0
        assert obj.main.name == "Jet0"
        assert obj.main.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Jet",
            "index": 0,
        }

        assert obj.sub.type == "Constituents"
        assert obj.sub.start == 1
        assert obj.sub.end is None
        assert obj.sub.name == "Constituents1:"
        assert obj.sub.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Constituents",
            "start": 1,
            "end": None,
        }

        assert obj.name == "Jet0.Constituents1:"
        assert obj.config == {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Jet",
                "index": 0,
            },
            "sub_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Constituents",
                "start": 1,
                "end": None,
            },
        }


def test_pattern_collective_single():
    obj1 = NestedPhysicsObject(
        CollectivePhysicsObject("Jet", 0),
        SinglePhysicsObject("Constituents", 1),
    )
    obj2 = NestedPhysicsObject.from_name("Jet0:.Constituents1")
    obj3 = NestedPhysicsObject.from_config(
        {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Jet",
                "start": 0,
                "end": None,
            },
            "sub_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Constituents",
                "index": 1,
            },
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.main.type == "Jet"
        assert obj.main.start == 0
        assert obj.main.end is None
        assert obj.main.name == "Jet0:"
        assert obj.main.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": None,
        }

        assert obj.sub.type == "Constituents"
        assert obj.sub.index == 1
        assert obj.sub.name == "Constituents1"
        assert obj.sub.config == {
            "class_name": "SinglePhysicsObject",
            "type": "Constituents",
            "index": 1,
        }

        assert obj.name == "Jet0:.Constituents1"
        assert obj.config == {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Jet",
                "start": 0,
                "end": None,
            },
            "sub_config": {
                "class_name": "SinglePhysicsObject",
                "type": "Constituents",
                "index": 1,
            },
        }


def test_pattern_collective_collective():
    obj1 = NestedPhysicsObject(
        CollectivePhysicsObject("Jet", 0),
        CollectivePhysicsObject("Constituents", 1),
    )
    obj2 = NestedPhysicsObject.from_name("Jet0:.Constituents1:")
    obj3 = NestedPhysicsObject.from_config(
        {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Jet",
                "start": 0,
                "end": None,
            },
            "sub_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Constituents",
                "start": 1,
                "end": None,
            },
        }
    )

    for obj in [obj1, obj2, obj3]:
        assert obj.main.type == "Jet"
        assert obj.main.start == 0
        assert obj.main.end is None
        assert obj.main.name == "Jet0:"
        assert obj.main.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Jet",
            "start": 0,
            "end": None,
        }

        assert obj.sub.type == "Constituents"
        assert obj.sub.start == 1
        assert obj.sub.end is None
        assert obj.sub.name == "Constituents1:"
        assert obj.sub.config == {
            "class_name": "CollectivePhysicsObject",
            "type": "Constituents",
            "start": 1,
            "end": None,
        }

        assert obj.name == "Jet0:.Constituents1:"
        assert obj.config == {
            "class_name": "NestedPhysicsObject",
            "main_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Jet",
                "start": 0,
                "end": None,
            },
            "sub_config": {
                "class_name": "CollectivePhysicsObject",
                "type": "Constituents",
                "start": 1,
                "end": None,
            },
        }


def test_bad_name():
    with pytest.raises(ValueError):
        NestedPhysicsObject.from_name("Jet0")


def test_bad_config():
    with pytest.raises(ValueError):
        NestedPhysicsObject.from_config(
            {
                "class_name": None,
                "main_config": {
                    "class_name": "SinglePhysicsObject",
                    "type": "Jet",
                    "index": 0,
                },
                "sub_config": {
                    "class_name": "SinglePhysicsObject",
                    "type": "Constituents",
                    "index": 1,
                },
            }
        )

import pytest

from hml.physics_objects import Collective
from hml.physics_objects import Multiple
from hml.physics_objects import Nested
from hml.physics_objects import Single
from hml.physics_objects import is_multiple


def test_init():
    obj = Multiple(
        physics_objects=[
            Single(branch="Jet", index=0),
            Collective(branch="Jet", start=1, stop=3),
            Nested(
                main=Single(branch="Jet", index=0),
                sub=Collective(branch="Constituents", stop=5),
            ),
        ]
    )

    # Attributes ------------------------------------------------------------- #
    assert len(obj.physics_objects) == 3

    assert obj.name == "Jet0,Jet1:3,Jet0.Constituents:5"
    assert obj.objects == [None, None, None]
    assert obj.config == {
        "physics_object_0": {
            "class_name": "Single",
            "config": {"branch": "Jet", "index": 0},
        },
        "physics_object_1": {
            "class_name": "Collective",
            "config": {"branch": "Jet", "start": 1, "stop": 3},
        },
        "physics_object_2": {
            "class_name": "Nested",
            "config": {
                "main": {
                    "class_name": "Single",
                    "config": {"branch": "Jet", "index": 0},
                },
                "sub": {
                    "class_name": "Collective",
                    "config": {"branch": "Constituents", "start": 0, "stop": 5},
                },
            },
        },
    }


def test_special_methods():
    obj = Multiple(
        physics_objects=[
            Single(branch="Jet", index=0),
            Collective(branch="Jet", start=1, stop=3),
            Nested(
                main=Single(branch="Jet", index=0),
                sub=Collective(branch="Constituents", stop=5),
            ),
        ]
    )

    # __eq__ ----------------------------------------------------------------- #
    assert (
        Multiple(
            physics_objects=[
                Single(branch="Jet", index=0),
                Collective(branch="Jet", start=1, stop=3),
                Nested(
                    main=Single(branch="Jet", index=0),
                    sub=Collective(branch="Constituents", stop=5),
                ),
            ]
        )
        == obj
    )

    # __repr__ --------------------------------------------------------------- #
    assert (
        repr(obj)
        == "Multiple(name='Jet0,Jet1:3,Jet0.Constituents:5', objects=[None, None, None])"
    )


def test_class_methods():
    obj = Multiple(
        physics_objects=[
            Single(branch="Jet", index=0),
            Collective(branch="Jet", start=1, stop=3),
            Nested(
                main=Single(branch="Jet", index=0),
                sub=Collective(branch="Constituents", stop=5),
            ),
        ]
    )

    # from_name -------------------------------------------------------------- #
    assert obj == Multiple.from_name("Jet0,Jet1:3,Jet0.Constituents:5")

    # from_config ------------------------------------------------------------ #
    assert obj == Multiple.from_config(obj.config)


def test_read_ttree(event):
    obj = Multiple(
        physics_objects=[
            Single(branch="Jet", index=0),
            Collective(branch="Jet", start=1, stop=3),
            Nested(
                main=Single(branch="Jet", index=0),
                sub=Collective(branch="Constituents", stop=5),
            ),
        ]
    )
    obj.read_ttree(event)

    assert len(obj.physics_objects[0].objects) == 1
    assert len(obj.physics_objects[1].objects) == 2
    assert len(obj.physics_objects[2].objects) == 1
    assert len(obj.physics_objects[2].objects[0]) == 5


def test_is_multiple(single_names, collective_names, nested_names, multiple_names):
    # Valid cases ------------------------------------------------------------ #
    for case in multiple_names:
        assert is_multiple(case) is True

    assert is_multiple("Jet0,Jet:", ["single", "collective", "nested"]) is True

    # Invalid cases ---------------------------------------------------------- #
    for case in single_names:
        assert is_multiple(case) is False

    for case in collective_names:
        assert is_multiple(case) is False

    for case in nested_names:
        assert is_multiple(case) is False

    assert is_multiple("Jet0,Jet:", ["single"]) is False
    assert is_multiple("Jet0,Jet:,Jet0.Constituents:", ["collective"]) is False
    assert is_multiple("Jet0,Jet:,Jet0.Constituents:", ["nested"]) is False

    with pytest.raises(ValueError):
        is_multiple("Jet0,Jet1", ["unknown"])

    with pytest.raises(ValueError):
        Multiple.from_name("Jet,Electron")

from hml.physics_objects import Collective
from hml.physics_objects import Nested
from hml.physics_objects import Single
from hml.physics_objects import is_nested


def test_init():
    obj = Nested(
        main=Single(branch="Jet", index=0),
        sub=Collective(branch="Constituents", start=1, stop=3),
    )

    # Attributes ------------------------------------------------------------- #
    assert obj.main.branch == "Jet"
    assert obj.main.index == 0

    assert obj.sub.branch == "Constituents"
    assert obj.sub.start == 1
    assert obj.sub.stop == 3

    assert obj.name == "Jet0.Constituents1:3"
    assert obj.objects is None
    assert obj.config == {
        "main": {
            "class_name": "Single",
            "config": {"branch": "Jet", "index": 0},
        },
        "sub": {
            "class_name": "Collective",
            "config": {
                "branch": "Constituents",
                "start": 1,
                "stop": 3,
            },
        },
    }


def test_special_methods():
    obj = Nested(
        main=Single(branch="Jet", index=0),
        sub=Collective(branch="Constituents", start=1, stop=3),
    )

    # __eq__ ----------------------------------------------------------------- #
    assert (
        Nested(
            main=Single(branch="Jet", index=0),
            sub=Collective(branch="Constituents", start=1, stop=3),
        )
        == obj
    )

    # __repr__ --------------------------------------------------------------- #
    assert repr(obj) == "Nested(name='Jet0.Constituents1:3', objects=None)"


def test_class_methods():
    obj = Nested(
        main=Single(branch="Jet", index=0),
        sub=Collective(branch="Constituents", start=1, stop=3),
    )

    # from_name -------------------------------------------------------------- #
    assert obj == Nested.from_name("Jet0.Constituents1:3")

    # from_config ------------------------------------------------------------ #
    assert obj == Nested.from_config(obj.config)


def test_read_ttree(event):
    # Common cases ----------------------------------------------------------- #
    obj = Nested.from_name("Jet0.Constituents0").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (1, 1)
    assert None not in obj.objects[0]

    obj = Nested.from_name("Jet0.Constituents:3").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (1, 3)
    assert None not in obj.objects[0]

    obj = Nested.from_name("Jet:3.Constituents:3").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (3, 3)
    assert None not in [j for i in obj.objects for j in i]

    # Edge cases ------------------------------------------------------------- #
    obj = Nested.from_name("Jet0.Constituents100").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (1, 0)
    assert obj.objects == [[]]

    # None-filled cases
    obj = Nested.from_name("Jet0.Constituents:100").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (1, 100)
    assert all([j for i in obj.objects for j in i]) is False
    assert any([j for i in obj.objects for j in i]) is True

    obj = Nested.from_name("Jet0.Constituents100:").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (1, 0)
    assert obj.objects == [[]]

    obj = Nested.from_name("Jet100.Constituents0").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100.Constituents100").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100.Constituents:100").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100.Constituents100:").read_ttree(event)
    assert obj.objects == []

    # None-filled cases
    obj = Nested.from_name("Jet:100.Constituents0").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (100, 1)
    for i in obj.objects:
        assert len(i) in [0, 1]

    obj = Nested.from_name("Jet:100.Constituents100").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (100, 0)
    assert [j for i in obj.objects for j in i] == []

    # None-filled cases
    obj = Nested.from_name("Jet:100.Constituents:100").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (100, 100)
    assert all([j for i in obj.objects for j in i]) is False
    assert any([j for i in obj.objects for j in i]) is True

    obj = Nested.from_name("Jet:100.Constituents100:").read_ttree(event)
    assert (len(obj.objects), len(obj.objects[0])) == (100, 0)
    assert [j for i in obj.objects for j in i] == []

    obj = Nested.from_name("Jet100:.Constituents0").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100:.Constituents100").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100:.Constituents:100").read_ttree(event)
    assert obj.objects == []

    obj = Nested.from_name("Jet100:.Constituents100:").read_ttree(event)
    assert obj.objects == []


def test_is_nested(single_names, collective_names, nested_names, multiple_names):
    # Valid cases ------------------------------------------------------------ #
    for case in nested_names:
        assert is_nested(case) is True

    # Invalid cases ---------------------------------------------------------- #
    for case in single_names:
        assert is_nested(case) is False

    for case in collective_names:
        assert is_nested(case) is False

    for case in multiple_names:
        assert is_nested(case) is False

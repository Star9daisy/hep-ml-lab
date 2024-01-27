from hml.physics_objects import Collective
from hml.physics_objects import Nested
from hml.physics_objects import Single
from hml.physics_objects import is_nested


def test_init():
    obj = Nested(
        main=Single(branch="Jet", index=0),
        sub=Collective(branch="Constituents", start=1, stop=3),
    )

    # Parameters ------------------------------------------------------------- #
    assert obj.main.branch == "Jet"
    assert obj.main.index == 0

    assert obj.sub.branch == "Constituents"
    assert obj.sub.start == 1
    assert obj.sub.stop == 3

    # Attributes ------------------------------------------------------------- #
    assert obj.name == "Jet0.Constituents1:3"
    assert obj.value is None


def test_read_ttree(event):
    # Valid cases ------------------------------------------------------------ #
    obj = Nested.from_name("Jet0.Constituents0").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 1)
    assert obj.value[0][0] is not None

    obj = Nested.from_name("Jet0.Constituents:3").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 3)
    assert all(obj.value[0]) is True

    obj = Nested.from_name("Jet:3.Constituents:3").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (3, 3)
    assert all([j for i in obj.value for j in i]) is True

    # Invalid cases ---------------------------------------------------------- #
    obj = Nested.from_name("Jet0.Constituents100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 1)
    assert obj.value[0][0] is None

    # None-filled cases
    obj = Nested.from_name("Jet0.Constituents:100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 100)
    assert all([j for i in obj.value for j in i]) is False
    assert any([j for i in obj.value for j in i]) is True

    obj = Nested.from_name("Jet0.Constituents100:").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 0)
    assert obj.value[0] == []

    obj = Nested.from_name("Jet100.Constituents0").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 1)
    assert obj.value[0][0] is None

    obj = Nested.from_name("Jet100.Constituents100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 1)
    assert obj.value[0][0] is None

    obj = Nested.from_name("Jet100.Constituents:100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 100)
    assert any([j for i in obj.value for j in i]) is False

    obj = Nested.from_name("Jet100.Constituents100:").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (1, 0)
    assert obj.value[0] == []

    # None-filled cases
    obj = Nested.from_name("Jet:100.Constituents0").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (100, 1)
    assert all([j for i in obj.value for j in i]) is False
    assert any([j for i in obj.value for j in i]) is True

    obj = Nested.from_name("Jet:100.Constituents100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (100, 1)
    assert any([j for i in obj.value for j in i]) is False

    # None-filled cases
    obj = Nested.from_name("Jet:100.Constituents:100").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (100, 100)
    assert all([j for i in obj.value for j in i]) is False
    assert any([j for i in obj.value for j in i]) is True

    obj = Nested.from_name("Jet:100.Constituents100:").read_ttree(event)
    assert (len(obj.value), len(obj.value[0])) == (100, 0)
    assert [j for i in obj.value for j in i] == []

    obj = Nested.from_name("Jet100:.Constituents0").read_ttree(event)
    assert obj.value == []

    obj = Nested.from_name("Jet100:.Constituents100").read_ttree(event)
    assert obj.value == []

    obj = Nested.from_name("Jet100:.Constituents:100").read_ttree(event)
    assert obj.value == []

    obj = Nested.from_name("Jet100:.Constituents100:").read_ttree(event)
    assert obj.value == []


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

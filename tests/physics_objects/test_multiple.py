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

    # Parameters ------------------------------------------------------------- #
    assert len(obj.physics_objects) == 3

    # Attributes ------------------------------------------------------------- #
    assert obj.name == "Jet0,Jet1:3,Jet0.Constituents:5"
    assert obj.value is None


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

    assert obj.physics_objects[0].value is not None
    assert any(obj.physics_objects[1].value) is True
    assert any([j for i in obj.physics_objects[2].value for j in i]) is True


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

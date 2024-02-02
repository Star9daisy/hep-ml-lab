import pytest

from hml.physics_objects.collective import Collective
from hml.physics_objects.collective import is_collective


def test_init():
    obj = Collective(branch="Jet", start=1, stop=3)

    # Attributes ------------------------------------------------------------- #
    assert obj.branch == "Jet"
    assert obj.start == 1
    assert obj.stop == 3
    assert obj.name == "Jet1:3"
    assert obj.objects is None
    assert obj.config == {"branch": "Jet", "start": 1, "stop": 3}

    # other names
    assert Collective(branch="Jet").name == "Jet:"
    assert Collective(branch="Jet", start=1).name == "Jet1:"
    assert Collective(branch="Jet", stop=3).name == "Jet:3"


def test_special_methods():
    obj = Collective(branch="Jet", start=1, stop=3)

    # __eq__ ----------------------------------------------------------------- #
    assert Collective(branch="Jet", start=1) == Collective(branch="Jet", start=1)

    # __repr__ --------------------------------------------------------------- #
    assert repr(obj) == "Collective(name='Jet1:3', objects=None)"


def test_class_methods():
    obj = Collective(branch="Jet", start=1, stop=3)

    # from_name -------------------------------------------------------------- #
    assert obj == Collective.from_name("Jet1:3")

    # from_config ------------------------------------------------------------ #
    assert obj == Collective.from_config(obj.config)


def test_read_ttree(event):
    # Common cases ----------------------------------------------------------- #
    obj = Collective(branch="Jet").read_ttree(event)
    assert len(obj.objects) > 0
    assert None not in obj.objects

    obj = Collective(branch="Jet", stop=3).read_ttree(event)
    assert len(obj.objects) == 3
    assert None not in obj.objects

    obj = Collective(branch="Jet", stop=10).read_ttree(event)
    assert len(obj.objects) == 10
    assert None in obj.objects

    obj = Collective(branch="Constituents", stop=3).read_ttree(event.Jet[0])
    assert len(obj.objects) == 3
    assert None not in obj.objects

    # Edge cases ------------------------------------------------------------- #
    obj = Collective(branch="Jet", start=100).read_ttree(event)
    assert len(obj.objects) == 0
    assert obj.objects == []

    obj = Collective(branch="Jet", start=100, stop=102).read_ttree(event)
    assert len(obj.objects) == 2
    assert obj.objects == [None, None]

    # Error cases ------------------------------------------------------------ #
    with pytest.raises(ValueError):
        Collective(branch="Unknown").read_ttree(event)


def test_is_collective(single_names, collective_names, nested_names, multiple_names):
    # Valid cases ------------------------------------------------------------ #
    for case in collective_names:
        assert is_collective(case) is True

    # Invalid cases ---------------------------------------------------------- #
    for case in single_names:
        assert is_collective(case) is False

    for case in nested_names:
        assert is_collective(case) is False

    for case in multiple_names:
        assert is_collective(case) is False

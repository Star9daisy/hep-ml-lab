from hml.physics_objects.collective import Collective
from hml.physics_objects.collective import is_collective


def test_init():
    obj = Collective(branch="Jet", start=1, stop=3)

    # Parameters ------------------------------------------------------------- #
    assert obj.branch == "Jet"
    assert obj.start == 1
    assert obj.stop == 3

    # Attributes ------------------------------------------------------------- #
    assert obj.name == "Jet1:3"
    assert obj.value is None
    assert obj.config == {"branch": "Jet", "start": 1, "stop": 3}

    # other names
    assert Collective(branch="Jet").name == "Jet:"
    assert Collective(branch="Jet", start=1).name == "Jet1:"
    assert Collective(branch="Jet", stop=3).name == "Jet:3"


def test_class_methods():
    obj = Collective(branch="Jet", start=1, stop=3)
    assert repr(obj) == "Collective(name='Jet1:3', value=None)"
    assert obj == Collective.from_name("Jet1:3")
    assert obj == Collective.from_config(obj.config)


def test_read_ttree(event):
    # Valid cases ------------------------------------------------------------ #
    obj = Collective(branch="Jet", stop=3).read_ttree(event)
    assert all(obj.value) is True

    obj = Collective(branch="Constituents", stop=3).read_ttree(event.Jet[0])
    assert all(obj.value) is True

    # Invalid cases ---------------------------------------------------------- #
    obj = Collective(branch="Jet", start=100).read_ttree(event)
    assert obj.value == []

    obj = Collective(branch="Jet", start=100, stop=102).read_ttree(event)
    assert len(obj.value) == 2
    assert obj.value == [None, None]

    # None-filled cases
    obj = Collective(branch="Jet", stop=100).read_ttree(event)
    assert len(obj.value) == 100
    assert any(obj.value) is True
    assert all(obj.value) is False


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

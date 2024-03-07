import pytest

from hml.physics_objects.collective import Collective, is_collective


def test_init():
    obj = Collective(branch="jet", start=1, stop=3)

    assert obj.branch == "jet"
    assert obj.start == 1
    assert obj.stop == 3
    assert obj.slices == [slice(1, 3)]
    assert obj.name == "jet1:3"
    assert obj.config == {"branch": "jet", "start": 1, "stop": 3}

    # other names
    assert Collective(branch="jet").name == "jet"
    assert Collective(branch="jet", start=1).name == "jet1:"
    assert Collective(branch="jet", stop=3).name == "jet:3"


def test_special_methods():
    obj = Collective(branch="jet", start=1, stop=3)

    assert obj == Collective(branch="jet", start=1, stop=3)
    assert str(obj) == "jet1:3"
    assert repr(obj) == "Collective(branch='jet', start=1, stop=3)"


def test_class_methods():
    obj = Collective(branch="jet", start=1, stop=3)

    assert obj == Collective.from_name("jet1:3")
    assert obj == Collective.from_config(obj.config)

    with pytest.raises(ValueError):
        Collective.from_name("jet0")


def test_is_collective(single_names, collective_names, nested_names):
    assert is_collective(None) is False

    assert is_collective(Collective(branch="jet", start=1, stop=3)) is True

    for case in collective_names:
        assert is_collective(case) is True

    for case in single_names:
        assert is_collective(case) is False

    for case in nested_names:
        assert is_collective(case) is False

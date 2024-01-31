from hml.physics_objects.single import Single
from hml.physics_objects.single import is_single


def test_init():
    obj = Single(branch="Jet", index=0)

    # Parameters ------------------------------------------------------------- #
    assert obj.branch == "Jet"
    assert obj.index == 0

    # Attributes ------------------------------------------------------------- #
    assert obj.name == "Jet0"
    assert obj.value is None
    assert obj.config == {"branch": "Jet", "index": 0}


def test_class_methods():
    obj = Single(branch="Jet", index=0)
    assert repr(obj) == "Single(name='Jet0', value=None)"
    assert obj == Single.from_name("Jet0")
    assert obj == Single.from_config(obj.config)


def test_read_ttree(event):
    # Valid cases ------------------------------------------------------------ #
    obj = Single(branch="Jet", index=0).read_ttree(event)
    assert obj.value is not None

    obj = Single(branch="Constituents", index=0).read_ttree(event.Jet[0])
    assert obj.value is not None

    # Invalid cases ---------------------------------------------------------- #
    obj = Single(branch="Jet", index=100).read_ttree(event)
    assert obj.value is None

    obj = Single(branch="Constituents", index=100).read_ttree(event.Jet[0])
    assert obj.value is None


def test_is_single(single_names, collective_names, nested_names, multiple_names):
    # Valid cases ------------------------------------------------------------ #
    for case in single_names:
        assert is_single(case) is True

    # Invalid cases ---------------------------------------------------------- #
    for case in collective_names:
        assert is_single(case) is False

    for case in nested_names:
        assert is_single(case) is False

    for case in multiple_names:
        assert is_single(case) is False

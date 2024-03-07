from itertools import combinations, product

import pytest

from hml.physics_objects import Collective, Multiple, Nested, Single, is_multiple


def test_init():
    obj = Multiple(
        objects=[Single(branch="jet", index=0), "jet", "jet0.constituents:3"]
    )

    assert len(obj.all) == 3
    assert obj.all[0] == Single(branch="jet", index=0)
    assert obj.all[1] == Collective(branch="jet")
    assert obj.all[2] == Nested(main="jet0", sub="constituents:3")

    assert obj.name == "jet0,jet,jet0.constituents:3"
    assert obj.config == {"objects": ["jet0", "jet", "jet0.constituents:3"]}


def test_special_methods():
    obj = Multiple(objects=["jet0", "jet", "jet0.constituents:3"])

    assert obj == Multiple(objects=["jet0", "jet", "jet0.constituents:3"])
    assert str(obj) == "jet0,jet,jet0.constituents:3"
    assert repr(obj) == "Multiple(objects=['jet0', 'jet', 'jet0.constituents:3'])"


def test_class_methods():
    obj = Multiple(objects=["jet0", "jet", "jet0.constituents:3"])

    assert obj == Multiple.from_name("jet0,jet,jet0.constituents:3")
    assert obj == Multiple.from_config(obj.config)

    with pytest.raises(ValueError):
        Multiple.from_name("jet0")


def test_is_multiple(single_names, collective_names, nested_names, multiple_names):
    assert is_multiple(None) is False

    assert is_multiple(Multiple(objects=["jet0", "jet", "jet0.constituents:3"])) is True

    for case in multiple_names:
        assert is_multiple(case) is True

    for case in single_names:
        assert is_multiple(case) is False

    for case in collective_names:
        assert is_multiple(case) is False

    for case in nested_names:
        assert is_multiple(case) is False

    for case in combinations(single_names, 2):
        assert is_multiple(",".join(case), ["single"]) is True

    for case in combinations(collective_names, 2):
        assert is_multiple(",".join(case), ["collective"]) is True

    for case in combinations(nested_names, 2):
        assert is_multiple(",".join(case), ["nested"]) is True

    for case in product(single_names, collective_names):
        assert is_multiple(",".join(case), ["single", "collective"]) is True
        assert is_multiple(",".join(case), ["single", "nested"]) is False

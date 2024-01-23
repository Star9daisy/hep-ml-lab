import pytest

from .collective import is_collective
from .multiple import is_multiple
from .nested import is_nested
from .single import is_single

test_single_cases = ["Jet0"]
test_collective_cases = ["Jet:", "Jet1:", "Jet:3", "Jet1:3"]
test_nested_cases = [
    "Jet0.Particles0",
    "Jet0.Particles:",
    "Jet0.Particles1:",
    "Jet0.Particles:3",
    "Jet0.Particles1:3",
    "Jet:.Particles:",
    "Jet:.Particles1:",
    "Jet:.Particles:3",
    "Jet:.Particles1:3",
    "Jet1:.Particles:",
    "Jet1:.Particles1:",
    "Jet1:.Particles:3",
    "Jet1:.Particles1:3",
    "Jet:3.Particles:",
    "Jet:3.Particles1:",
    "Jet:3.Particles:3",
    "Jet:3.Particles1:3",
    "Jet1:3.Particles:",
    "Jet1:3.Particles1:",
    "Jet1:3.Particles:3",
    "Jet1:3.Particles1:3",
]
test_multiple_cases = [
    "Jet0,Jet1",
    "Jet0,Jet1,Jet2",
    "Jet0,Jet:",
    "Jet0,Jet0.Particles:",
    "Jet0.Particles:,Jet0.Particles:",
]


def test_is_single():
    for case in test_single_cases:
        assert is_single(case) is True

    for case in test_collective_cases:
        assert is_single(case) is False

    for case in test_nested_cases:
        assert is_single(case) is False

    for case in test_multiple_cases:
        assert is_single(case) is False


def test_is_collective():
    for case in test_single_cases:
        assert is_collective(case) is False

    for case in test_collective_cases:
        assert is_collective(case) is True

    for case in test_nested_cases:
        assert is_collective(case) is False

    for case in test_multiple_cases:
        assert is_collective(case) is False


def test_is_nested():
    for case in test_single_cases:
        assert is_nested(case) is False

    for case in test_collective_cases:
        assert is_nested(case) is False

    for case in test_nested_cases:
        assert is_nested(case) is True

    for case in test_multiple_cases:
        assert is_nested(case) is False


def test_is_multiple():
    for case in test_single_cases:
        assert is_multiple(case) is False

    for case in test_collective_cases:
        assert is_multiple(case) is False

    for case in test_nested_cases:
        assert is_multiple(case) is False

    for case in test_multiple_cases:
        assert is_multiple(case) is True


def test_is_multiple_with_supported_types():
    assert is_multiple("Jet0,Jet1", ["single"]) is True
    assert is_multiple("Jet0,Jet1", ["collective"]) is False
    assert is_multiple("Jet0,Jet1", ["nested"]) is False

    with pytest.raises(ValueError):
        is_multiple("Jet0,Jet1", ["unknown"])

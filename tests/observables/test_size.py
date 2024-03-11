import pytest

from hml.observables.size import Size


def test_init():
    obs = Size(physics_object="Jet")

    assert obs.physics_object.name == "Jet"
    assert obs.class_name == "Size"

    assert obs.name == "Jet.Size"
    assert len(obs.value) == 0
    assert obs.config == {
        "physics_object": obs.physics_object.name,
        "class_name": "Size",
    }


def test_class_methods():
    obs = Size(physics_object="Jet")

    assert obs == Size.from_name("Jet.Size")
    assert obs == Size.from_config(obs.config)

    with pytest.raises(ValueError):
        Size.from_name("Jet0")


def test_read(events):
    obs = Size("Jet").read(events)
    assert str(obs.value.type) == "100 * int32"

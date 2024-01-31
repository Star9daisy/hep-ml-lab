from math import isnan

import pytest

from hml.observables.angular_distance import AngularDistance
from hml.observables.angular_distance import DeltaR


def test_attributes():
    obs = AngularDistance(physics_object="Jet0,Jet1")

    # Parameters ------------------------------------------------------------- #
    assert obs.physics_object.name == "Jet0,Jet1"
    assert obs.supported_types == ["single", "collective", "nested", "multiple"]

    # Attributes ------------------------------------------------------------- #
    assert obs.name == "Jet0,Jet1.AngularDistance"
    assert isnan(obs.value)
    assert obs.shape == "1 * float64"
    assert obs.config == {"physics_object": obs.physics_object.name}

    with pytest.raises(ValueError):
        AngularDistance(physics_object="Jet0,Jet1,Jet2")


def test_class_methods():
    obs = AngularDistance(physics_object="Jet0,Jet1")

    assert repr(obs) == "Jet0,Jet1.AngularDistance : nan"
    assert obs == AngularDistance.from_name("Jet0,Jet1.AngularDistance")


def test_read(event):
    obj = DeltaR("Jet0,Jet1").read_ttree(event)
    assert obj.shape == "1 * 1 * float64"
    assert obj.value[0][0] is not None

    obj = DeltaR("Jet0,Jet1.Constituents100:").read_ttree(event)
    assert obj.shape == "1 * 0 * unknown"
    assert obj.value[0] == []

    obj = DeltaR("Jet0,Jet100.Constituents100:").read_ttree(event)
    assert obj.shape == "1 * 0 * unknown"
    assert obj.value[0] == []
